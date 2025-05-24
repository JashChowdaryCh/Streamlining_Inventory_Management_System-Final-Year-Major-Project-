from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import serial
import threading
import time
import pandas as pd
import os
import joblib
import warnings
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

app = Flask(__name__)
CORS(app)

# Global variables for Arduino data
arduino_data = {
    'temperature': 0,
    'humidity': 0,
    'mq3_value': 0,
    'ldr_value': 0
}
arduino_connected = False
serial_thread = None

# Suppress warnings
warnings.simplefilter("ignore")

# Load datasets
stock_file = "textile_stock_dataset.csv"
demand_file = "textile_demand_dataset.csv"
restock_file = "restock_requests.csv"
fabric_waste_file = "Fabric_Waste_Data.csv"

try:
    stock_df = pd.read_csv(stock_file)
    demand_df = pd.read_csv(demand_file)
    fabric_data = pd.read_csv(fabric_waste_file)
except FileNotFoundError as e:
    print(f"Error loading dataset files: {e}")
    exit(1)

# Clean column names
stock_df.columns = stock_df.columns.str.strip()
demand_df.columns = demand_df.columns.str.strip()
fabric_data.columns = fabric_data.columns.str.strip()

stock_df = stock_df.map(lambda x: x.strip() if isinstance(x, str) else x)
demand_df = demand_df.map(lambda x: x.strip() if isinstance(x, str) else x)
fabric_data = fabric_data.map(lambda x: x.strip() if isinstance(x, str) else x)

# Convert 'Fabric Type' to lowercase
stock_df["Fabric Type"] = stock_df["Fabric Type"].str.lower()
demand_df["Fabric Type"] = demand_df["Fabric Type"].str.lower()
fabric_data["Fabric"] = fabric_data["Fabric"].str.lower()

# Define valid categories from dataset
valid_seasons = ["Summer", "All-Season", "Winter", "Rainy"]
valid_occasions = ["Casual", "Ethnic", "Formal", "Sportswear", "Workwear"]
valid_budgets = ["Low", "Medium", "High"]

# Encode categorical columns for fabric recycling
label_encoder = LabelEncoder()
fabric_data["Biodegradable"] = label_encoder.fit_transform(fabric_data["Biodegradable"])
fabric_data["Recyclable"] = label_encoder.fit_transform(fabric_data["Recyclable"])
fabric_data["Disposal Method"] = label_encoder.fit_transform(fabric_data["Disposal Method"])

# Train Random Forest model
X = fabric_data[["Biodegradable", "Recyclable", "Monthly_Waste_kg", "Annual_Trend"]]
y = fabric_data["Disposal Method"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Save model
joblib.dump(rf_model, "fabric_recycling_model.pkl")

LOW_STOCK_THRESHOLD = 100

def get_inventory_summary():
    total_fabrics = stock_df['Fabric Type'].nunique()
    current_inventory = stock_df['Stock Available'].sum()

    # Identify low stock fabrics
    low_stock_fabrics = stock_df[stock_df['Stock Available'] < LOW_STOCK_THRESHOLD]
    low_stock_count = len(low_stock_fabrics)
    low_stock_names = low_stock_fabrics['Fabric Type'].tolist()

    # Identify high-demand fabrics
    high_demand_fabrics = demand_df[demand_df['Current Demand'] > (demand_df['Historical Demand'] * 1.25)]
    high_demand_count = len(high_demand_fabrics)
    high_demand_names = high_demand_fabrics['Fabric Type'].tolist()

    return {
        'total_fabrics': total_fabrics,
        'current_inventory': current_inventory,
        'low_stock_count': low_stock_count,
        'low_stock_names': low_stock_names,
        'high_demand_count': high_demand_count,
        'high_demand_names': high_demand_names
    }

def get_stock_details(fabric_type):
    fabric_type = fabric_type.strip().lower()
    stock_info = stock_df[stock_df["Fabric Type"] == fabric_type]
    
    if stock_info.empty:
        return None
    
    return stock_info.iloc[0][["Price per Unit", "Stock Available", "Unit Type"]].to_dict()

def predict_price(fabric_type):
    df = demand_df[demand_df["Fabric Type"] == fabric_type]

    if df.empty:
        return None

    X = df[['Historical Demand', 'Current Demand']]
    y = df['Price per Unit']

    model = LinearRegression()
    model.fit(X, y)

    predicted_price = model.predict(pd.DataFrame([X.iloc[0].values], columns=X.columns))[0]
    
    india_high_demand = {"cotton", "silk", "denim", "polyester"}
    india_low_demand = {"wool", "linen", "rayon"}
    
    historical_demand = X.iloc[0, 0]
    current_demand = X.iloc[0, 1]

    if fabric_type in india_high_demand:
        demand_status = "High Demand"
    elif fabric_type in india_low_demand:
        demand_status = "Low Demand"
    else:
        if current_demand > historical_demand * 1.25:
            demand_status = "High Demand"
        elif current_demand < historical_demand * 0.75:
            demand_status = "Low Demand"
        else:
            demand_status = "Stable Demand"
    
    # Return consistent property names
    return {
        "predictedPrice": round(predicted_price, 2),
        "demandStatus": demand_status
    }

def recommend_fabrics(season, occasion, budget):
    season = season.lower()
    occasion = occasion.lower()
    budget = budget.lower()
    
    filtered_df = demand_df[
        (demand_df["Season"].str.lower() == season) &
        (demand_df["Occasion"].str.lower() == occasion) &
        (demand_df["Budget Category"].str.lower() == budget)
    ]
    
    if filtered_df.empty:
        filtered_df = demand_df[
            (demand_df["Season"].str.lower() == "all-season") &
            (demand_df["Occasion"].str.lower() == occasion) &
            (demand_df["Budget Category"].str.lower() == budget)
        ]
    
    return filtered_df["Fabric Type"].tolist() if not filtered_df.empty else ["No fabric recommendations available."]

def get_recycling_steps(fabric_name):
    fabric_row = fabric_data[fabric_data["Fabric"].str.lower() == fabric_name.lower().strip()]
    if fabric_row.empty:
        return f"Sorry, recycling information for '{fabric_name}' is not available."
    input_data = fabric_row[["Biodegradable", "Recyclable", "Monthly_Waste_kg", "Annual_Trend"]]
    predicted_method = rf_model.predict(input_data)[0]
    disposal_method = label_encoder.inverse_transform([predicted_method])[0]
    steps = [f"Recycling Guide for {fabric_name}"]
    steps.append("Step 1: Collect and separate clean fabric waste.")
    if fabric_row["Biodegradable"].values[0] == 1:
        steps.append("Step 2: If reusable, send for upcycling (convert into rags, bags, stuffing).")
        if disposal_method == "Composting":
            steps.append("Step 3: If not reusable, send for composting (fabric decomposes naturally).")
        elif disposal_method == "Chemical Recycling":
            steps.append("Step 3: Process through chemical recycling to extract reusable fibers.")
    else:
        if disposal_method == "Mechanical Recycling":
            steps.append("Step 2: Shred and process the fabric into recycled fibers.")
            steps.append("Step 3: Convert into new fabric materials for reuse.")
        elif disposal_method == "Incineration":
            steps.append("Step 2: If no recycling options are available, dispose of through incineration.")
    return "\n".join(steps)

def read_serial_data():
    global arduino_data, arduino_connected
    
    # Replace with your actual Arduino port
    arduino_port = 'COM3'
    baud_rate = 9600
    
    try:
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        arduino_connected = True
        print(f"Connected to {arduino_port} at {baud_rate} baud rate.")
        
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print("Raw:", line)
                
                try:
                    parts = line.split(',')
                    if len(parts) >= 4:
                        temperature = float(parts[0].split(':')[1].strip().replace('C', ''))
                        humidity = float(parts[1].split(':')[1].strip().replace('%', ''))
                        mq3_value = int(parts[2].split(':')[1].strip())
                        ldr_value = int(parts[3].split(':')[1].strip())
                        
                        arduino_data = {
                            'temperature': temperature,
                            'humidity': humidity,
                            'mq3_value': mq3_value,
                            'ldr_value': ldr_value
                        }
                    
                except (IndexError, ValueError) as e:
                    print("Error parsing line:", e)
                    
            time.sleep(0.1)
            
    except serial.SerialException as e:
        print("Error opening serial port:", e)
        arduino_connected = False
    except KeyboardInterrupt:
        print("Serial reading stopped by user.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")
            arduino_connected = False

# Start serial reading in a separate thread
def start_serial_thread():
    global serial_thread
    if serial_thread is None or not serial_thread.is_alive():
        serial_thread = threading.Thread(target=read_serial_data)
        serial_thread.daemon = True
        serial_thread.start()
        print("Serial thread started")

start_serial_thread()

@app.route('/')
def index():
    inventory = get_inventory_summary()
    return render_template('index.html', inventory=inventory, arduino_connected=arduino_connected)

@app.route('/arduino')
def arduino_page():
    return render_template('arduino.html', 
                         arduino_connected=arduino_connected,
                         initial_data=arduino_data)

@app.route('/get_arduino_data')
def get_arduino_data():
    return jsonify({
        'temperature': arduino_data['temperature'],
        'humidity': arduino_data['humidity'],
        'mq3_value': arduino_data['mq3_value'],
        'ldr_value': arduino_data['ldr_value'],
        'connected': arduino_connected
    })

@app.route('/check_stock', methods=['POST'])
def check_stock():
    fabric_type = request.form.get('fabric_type')
    stock_details = get_stock_details(fabric_type)
    if stock_details is None:
        return jsonify({'error': 'Fabric not found'})
    return jsonify(stock_details)

@app.route('/predict_price', methods=['POST'])
def predict_price_route():
    fabric_type = request.form.get('fabric_type')
    predicted_info = predict_price(fabric_type)
    if predicted_info is None:
        return jsonify({'error': 'Fabric not found'})
    
    # Ensure we're returning the exact same property names
    return jsonify({
        'predictedPrice': predicted_info['predictedPrice'],
        'demandStatus': predicted_info['demandStatus']
    })

@app.route('/recommend_fabrics', methods=['POST'])
def recommend_fabrics_route():
    season = request.form.get('season')
    occasion = request.form.get('occasion')
    budget = request.form.get('budget')
    recommendations = recommend_fabrics(season, occasion, budget)
    return jsonify({'recommendations': recommendations})

@app.route('/get_recycling_info', methods=['POST'])
def get_recycling_info():
    fabric_name = request.form.get('fabric_name')
    recycling_info = get_recycling_steps(fabric_name)
    return jsonify({'recycling_info': recycling_info})

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
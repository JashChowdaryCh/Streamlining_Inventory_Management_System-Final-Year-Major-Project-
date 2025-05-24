from flask import Flask, render_template, request
import pandas as pd
import joblib
import os
import warnings
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from flask_cors import CORS

warnings.simplefilter("ignore")

app = Flask(__name__)
CORS(app)

# Load datasets
stock_file = "textile_stock_dataset.csv"
demand_file = "textile_demand_dataset.csv"
restock_file = "restock_requests.csv"
fabric_waste_file = "Fabric_Waste_Data.csv"

stock_df = pd.read_csv(stock_file)
demand_df = pd.read_csv(demand_file)
fabric_data = pd.read_csv(fabric_waste_file)

# Clean data
stock_df.columns = stock_df.columns.str.strip()
demand_df.columns = demand_df.columns.str.strip()
fabric_data.columns = fabric_data.columns.str.strip()

stock_df = stock_df.map(lambda x: x.strip() if isinstance(x, str) else x)
demand_df = demand_df.map(lambda x: x.strip() if isinstance(x, str) else x)
fabric_data = fabric_data.map(lambda x: x.strip() if isinstance(x, str) else x)

stock_df["Fabric Type"] = stock_df["Fabric Type"].str.lower()
demand_df["Fabric Type"] = demand_df["Fabric Type"].str.lower()
fabric_data["Fabric"] = fabric_data["Fabric"].str.lower()

# Encode recycling columns
label_encoder = LabelEncoder()
fabric_data["Biodegradable"] = label_encoder.fit_transform(fabric_data["Biodegradable"])
fabric_data["Recyclable"] = label_encoder.fit_transform(fabric_data["Recyclable"])
fabric_data["Disposal Method"] = label_encoder.fit_transform(fabric_data["Disposal Method"])

# Train model
X = fabric_data[["Biodegradable", "Recyclable", "Monthly_Waste_kg", "Annual_Trend"]]
y = fabric_data["Disposal Method"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
joblib.dump(rf_model, "fabric_recycling_model.pkl")

# Helper Functions
def get_stock_details(fabric_type):
    fabric_type = fabric_type.strip().lower()
    stock_info = stock_df[stock_df["Fabric Type"] == fabric_type]
    if stock_info.empty:
        return None
    result = stock_info.iloc[0][["Price per Unit", "Stock Available", "Unit Type"]].to_dict()
    return result

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
    return {"Predicted Price": round(predicted_price, 2), "Demand Status": demand_status}

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

# Flask Routes
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/stock', methods=['GET', 'POST'])
def stock():
    result = None
    if request.method == 'POST':
        fabric = request.form['fabric']
        result = get_stock_details(fabric)
    return render_template("stock.html", result=result)

@app.route('/price', methods=['GET', 'POST'])
def price():
    result = None
    if request.method == 'POST':
        fabric_type = request.form['fabric_type']
        result = predict_price(fabric_type)
    return render_template("price.html", result=result)

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    fabrics = []
    if request.method == 'POST':
        season = request.form['season']
        occasion = request.form['occasion']
        budget = request.form['budget']
        fabrics = recommend_fabrics(season, occasion, budget)
    return render_template("recommend.html", fabrics=fabrics)

@app.route('/recycle', methods=['GET', 'POST'])
def recycle():
    steps = None
    if request.method == 'POST':
        fabric = request.form['fabric']
        steps = get_recycling_steps(fabric)
    return render_template("recycle.html", steps=steps)

if __name__ == '__main__':
    app.run(debug=True)

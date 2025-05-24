import pandas as pd
import os
import joblib
import warnings
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

warnings.simplefilter("ignore")

app = Flask(__name__)
CORS(app)

# Load datasets
stock_df = pd.read_csv("textile_stock_dataset.csv")
demand_df = pd.read_csv("textile_demand_dataset.csv")
fabric_data = pd.read_csv("Fabric_Waste_Data.csv")

# Clean data
stock_df.columns = stock_df.columns.str.strip()
demand_df.columns = demand_df.columns.str.strip()
fabric_data.columns = fabric_data.columns.str.strip()

for df in [stock_df, demand_df, fabric_data]:
    df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
stock_df["Fabric Type"] = stock_df["Fabric Type"].str.lower()

demand_df["Fabric Type"] = demand_df["Fabric Type"].str.lower()
fabric_data["Fabric"] = fabric_data["Fabric"].str.lower()

# Encode categorical columns
label_encoder = LabelEncoder()
fabric_data["Biodegradable"] = label_encoder.fit_transform(fabric_data["Biodegradable"])
fabric_data["Recyclable"] = label_encoder.fit_transform(fabric_data["Recyclable"])
fabric_data["Disposal Method"] = label_encoder.fit_transform(fabric_data["Disposal Method"])

X = fabric_data[["Biodegradable", "Recyclable", "Monthly_Waste_kg", "Annual_Trend"]]
y = fabric_data["Disposal Method"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
joblib.dump(rf_model, "fabric_recycling_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/stock", methods=["POST"])
def api_stock():
    fabric = request.form.get("fabric", "").strip().lower()
    print("Checking stock for:", fabric)  # Debug line
    if not fabric:
        return jsonify({"error": "No fabric provided"}), 400
    stock = get_stock_details(fabric)
    return jsonify(stock if stock else {"error": "Fabric not found"})


@app.route("/api/predict", methods=["POST"])
def api_predict():
    fabric = request.form.get("fabric", "").strip().lower()
    if not fabric:
        return jsonify({"error": "No fabric provided"}), 400
    prediction = predict_price(fabric)
    return jsonify(prediction if prediction else {"error": "Fabric not found"})


@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    season = request.form.get("season", "").strip()
    occasion = request.form.get("occasion", "").strip()
    budget = request.form.get("budget", "").strip()
    fabrics = recommend_fabrics(season, occasion, budget)
    return jsonify({"recommendations": fabrics})


@app.route("/api/recycle", methods=["POST"])
def api_recycle():
    fabric = request.form.get("fabric", "").strip()
    if not fabric:
        return jsonify({"error": "No fabric provided"}), 400
    steps = get_recycling_steps(fabric)
    return jsonify({"steps": steps})


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
    historical_demand = X.iloc[0, 0]
    current_demand = X.iloc[0, 1]

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
        return ["No fabric recommendations available."]
    return filtered_df["Fabric Type"].tolist()


def get_recycling_steps(fabric_name):
    model = joblib.load("fabric_recycling_model.pkl")
    fabric_row = fabric_data[fabric_data["Fabric"] == fabric_name.lower().strip()]
    if fabric_row.empty:
        return [f"Sorry, recycling information for '{fabric_name}' is not available."]

    input_data = fabric_row[["Biodegradable", "Recyclable", "Monthly_Waste_kg", "Annual_Trend"]]
    predicted_method = model.predict(input_data)[0]
    disposal_method = label_encoder.inverse_transform([predicted_method])[0]

    steps = [f"Recycling Guide for {fabric_name}"]
    steps.append("Step 1: Collect and separate clean fabric waste.")
    if fabric_row["Biodegradable"].values[0] == 1:
        steps.append("Step 2: If reusable, send for upcycling.")
        if disposal_method == "Composting":
            steps.append("Step 3: Compost the biodegradable fabric.")
        elif disposal_method == "Chemical Recycling":
            steps.append("Step 3: Send for chemical recycling.")
    else:
        if disposal_method == "Mechanical Recycling":
            steps.append("Step 2: Shred and convert into fibers.")
        elif disposal_method == "Incineration":
            steps.append("Step 2: Dispose using incineration.")
    return steps


if __name__ == "__main__":
    app.run(debug=True)

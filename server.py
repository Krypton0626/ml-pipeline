from flask import Flask, request, jsonify
import joblib
import numpy as np
import sqlite3
import logging
import datetime

# Initialize Flask app
app = Flask(__name__)

# Load trained model and scaler
model = joblib.load("models/model.pkl")
scaler = joblib.load("models/scaler.pkl")

# Setup logging
logging.basicConfig(filename="api_requests.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Connect to SQLite database
conn = sqlite3.connect("predictions.db", check_same_thread=False)
cursor = conn.cursor()

# Create table for storing predictions
cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        features TEXT,
        prediction INTEGER
    )
""")
conn.commit()


@app.route("/predict", methods=["POST"])
def predict():
    try:
        start_time = datetime.datetime.now()
        
        data = request.json["features"]
        data_array = np.array(data).reshape(1, -1)
        data_scaled = scaler.transform(data_array)
        prediction = model.predict(data_scaled)[0]

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Store prediction in SQLite database
        cursor.execute("INSERT INTO predictions (timestamp, features, prediction) VALUES (?, ?, ?)", 
                       (timestamp, str(data), int(prediction)))
        conn.commit()

        end_time = datetime.datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        logging.info(f"Timestamp: {timestamp}, Features: {data}, Prediction: {prediction}, Processing Time: {processing_time:.4f} sec")

        return jsonify({"timestamp": timestamp, "prediction": int(prediction)})
    
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)})
if __name__ == "__main__":
    app.run(debug=True)

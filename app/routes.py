import os
import joblib
import numpy as np
import pandas as pd
from flask import Blueprint, jsonify, render_template, request
import time
import random

main = Blueprint('main', __name__)

MODEL_PATH = 'models/model.pkl'
SCALER_PATH = 'models/scaler.pkl'
DATA_PATH = 'data/cleaned_creditcard.csv'

# Load the dataset once when the application starts
try:
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df)} records from dataset")
except Exception as e:
    print(f"Error loading dataset: {str(e)}")
    df = None

def load_models():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler

def get_random_transaction():
    if df is not None:
        # Randomly select a row from the dataset
        random_row = df.iloc[random.randint(0, len(df)-1)]
        # Convert to dictionary and handle numpy types
        transaction_dict = {}
        for k, v in random_row.to_dict().items():
            if isinstance(v, (np.floating, np.integer)):
                transaction_dict[k] = float(v)
            else:
                transaction_dict[k] = v
        
        # Ensure Time field is present
        if 'Time' not in transaction_dict:
            transaction_dict['Time'] = 0.0
            
        return transaction_dict
    return None

def make_prediction(features):
    try:
        model, scaler = load_models()
        # Scale the features
        scaled_features = scaler.transform(np.array(features).reshape(1, -1))
        # Get prediction and probability
        prediction = model.predict(scaled_features)
        probability = model.predict_proba(scaled_features)
        return prediction[0], probability[0]
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return None, None

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/get_random_data', methods=['GET'])
def random_data():
    try:
        transaction = get_random_transaction()
        if transaction:
            return jsonify({
                'status': 'success',
                'data': transaction
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Could not get random transaction'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debug print
        
        # Convert features to list in correct order for model
        feature_columns = ['Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10',
                         'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20',
                         'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'Amount']
        
        # Check if we received data in the correct format
        if not isinstance(data, dict):
            print("Invalid data format received:", data)
            return jsonify({
                'status': 'error',
                'message': 'Invalid data format'
            }), 400

        # Debug print for missing features
        missing_features = [col for col in feature_columns if col not in data]
        if missing_features:
            print("Missing features:", missing_features)
            return jsonify({
                'status': 'error',
                'message': f'Missing required features: {", ".join(missing_features)}'
            }), 400
            
        # Extract features in correct order
        try:
            features = [float(data[col]) for col in feature_columns]
        except (KeyError, ValueError) as e:
            print("Error extracting features:", str(e))
            return jsonify({
                'status': 'error',
                'message': f'Error processing features: {str(e)}'
            }), 400

        prediction, probabilities = make_prediction(features)
        
        if prediction is not None:
            response = {
                'status': 'success',
                'prediction': int(prediction),
                'probability': float(probabilities[1]),
                'confidence': float(max(probabilities))
            }
            print("Successful prediction:", response)
            return jsonify(response)
        else:
            return jsonify({
                'status': 'error',
                'message': 'Could not make prediction'
            }), 500
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Error handlers
@main.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

@main.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
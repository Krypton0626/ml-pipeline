import joblib
from pathlib import Path
import numpy as np

model = None

def init_model():
    global model
    model_path = Path('models/trained_model.pkl')
    if model_path.exists():
        model = joblib.load(model_path)
    else:
        raise FileNotFoundError("Model file not found. Please train the model first.")

def predict_single(features):
    if model is None:
        init_model()
    
    features_array = np.array(features).reshape(1, -1)
    prediction = model.predict(features_array)
    
    # Get prediction probabilities if available
    if hasattr(model, 'predict_proba'):
        confidence = model.predict_proba(features_array).max()
    else:
        confidence = 0.0
    
    return prediction[0], confidence
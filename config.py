# config.py
import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Data paths
    RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw')
    PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed')
    
    # Model paths
    MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model.pkl')
    SCALER_PATH = os.path.join(BASE_DIR, 'models', 'scaler.pkl')
    
    # Logging paths
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    API_LOG_PATH = os.path.join(LOG_DIR, 'api_requests.log')
    SERVER_LOG_PATH = os.path.join(LOG_DIR, 'server.log')
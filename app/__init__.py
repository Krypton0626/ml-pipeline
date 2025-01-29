from flask import Flask
from config import Config
import os  # Add this import at the top

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize logging
    if not os.path.exists(app.config['LOG_DIR']):
        os.makedirs(app.config['LOG_DIR'])
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app
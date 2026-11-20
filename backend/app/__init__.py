from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from mongoengine import connect
from dotenv import load_dotenv
import os
import sys

def flush_print(msg):
    print(msg)
    sys.stdout.flush()

load_dotenv()

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'nyaysetu-jwt-secret-2026'
    app.config['JWT_SECRET_KEY'] = 'nyaysetu-jwt-secret-2026'
    
    # MongoDB Connection
    flush_print("Connecting to MongoDB...")
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/nyaysetu_db')
    connected = False
    try:
        connect(host=mongo_uri, serverSelectionTimeoutMS=2000)
        from mongoengine.connection import get_db
        get_db().command('ping')
        flush_print("Connected to MongoDB successfully.")
        connected = True
    except Exception as e:
        flush_print(f"External MongoDB unavailable: {e}")
        flush_print("Falling back to In-Memory Mock Database (mongomock)...")
        try:
            import mongomock
            from mongoengine.connection import disconnect
            disconnect()
            connect(mongo_client_class=mongomock.MongoClient, db='nyaysetu_db')
            flush_print("Connected to In-Memory Mock MongoDB successfully.")
            connected = True
        except Exception as mock_err:
            flush_print(f"Error starting mongomock: {mock_err}")

    # Seed demo data if database is empty or in mock mode
    try:
        from app.demo_seeder import seed_demo_environment
        seed_demo_environment()
    except Exception as seed_err:
        flush_print(f"Seed info: {seed_err}")
    
    # Extensions
    jwt.init_app(app)
    CORS(app)
    flush_print("Flask app initialized with extensions.")
    
    # Blueprints
    from app.routes.auth import auth_bp
    from app.routes.cases import cases_bp
    from app.routes.laws import laws_bp
    from app.routes.notifications import notifications_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(cases_bp, url_prefix='/api/cases')
    app.register_blueprint(laws_bp, url_prefix='/api/laws')
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
    
    return app

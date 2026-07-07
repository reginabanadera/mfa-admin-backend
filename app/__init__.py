import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from database import db
import logging
from flask_sqlalchemy import SQLAlchemy
from app.services.encryption_services import generate_and_store_master_key

logging.basicConfig(filename='C:/inetpub/wwwroot/IT_MFAAuthentication/error.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

def create_app():
    app = Flask(__name__)
    
    #cors = CORS(app, origins=["http://localhost:5173"], supports_credentials=True )
    #CORS(app)  # Allows React to call API

    # Load environment variables
    load_dotenv() 

    app.secret_key = os.getenv("FLASK_SECRET_KEY")

    # Configure the SQLAlchemy database URI
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    db_driver = 'ODBC+Driver+17+for+SQL+Server'
                             
    db_uri = f"mssql+pyodbc://{db_user}:{db_password}@{db_host}/{db_name}?driver={db_driver}"
    
    # Configure the second (HRIS) database URI
    hris_db_name = os.getenv('HRIS_DB_NAME')  # Set this in your .env
    hris_db_uri = f"mssql+pyodbc://{db_user}:{db_password}@{db_host}/{hris_db_name}?driver={db_driver}"


    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    # Configure the second database with SQLALCHEMY_BINDS
    app.config['SQLALCHEMY_BINDS'] = {
        'hris_db': hris_db_uri  # Bind this URI to the 'hris_db' key
    }

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False  # Enable SQL logging
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600  # Recycle connections to avoid timeouts
    
    # This will handle all the db connections
    db.init_app(app)

    # Import and register blueprints (routes)
    from app.routes.auth import auth_bp
    # from app.routes.user import user_bp
    cors = CORS(auth_bp, origins=["http://localhost:5173"], supports_credentials=True )
    app.register_blueprint(auth_bp, url_prefix="/auth")
    # app.register_blueprint(user_bp, url_prefix="/user")

    with app.app_context():
        db.create_all()
        generate_and_store_master_key()

    return app
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # FIX: Flask-PyMongo requires MONGO_URI, not MONGODB_URI
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/studymate'
    
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

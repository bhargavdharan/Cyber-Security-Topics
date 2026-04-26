import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cybersec-platform-dev-key-2024')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-for-cybersec-platform')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # MySQL Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'Dharan@20')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'cybersec_platform')
    
    # CORS
    CORS_ORIGINS = ["http://localhost:5173", "http://localhost:3000"]

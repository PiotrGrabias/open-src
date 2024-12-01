import os

class Config:
    SECRET_KEY = os.urandom(24)  # Secure random key for sessions
    # Set the database URI for SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # SQLite URI (relative path)
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking to avoid overhead

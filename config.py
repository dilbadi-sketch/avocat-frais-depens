import os
from datetime import timedelta

# Configuration de base
class Config:
    """Configuration générale"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///avocat.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration de session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # True en production
    SESSION_COOKIE_HTTPONLY = True
    
    # Configuration de l'application
    APP_NAME = "Calculateur de Frais et Dépens"
    ITEMS_PER_PAGE = 20

class DevelopmentConfig(Config):
    """Configuration de développement"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuration de production"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Configuration de test"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Sélection de la configuration
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

from mass_flask_config.config_base import BaseConfig


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'mass-flask-development',
        'host': 'mongodb://localhost:27017/'
    }

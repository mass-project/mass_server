from mass_flask_config.config_base import BaseConfig


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'mass-flask-development',
        'host': 'localhost',
        'port': 27017,
        'tz_aware': True
    }

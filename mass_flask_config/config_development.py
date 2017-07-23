from mass_flask_config.config_base import BaseConfig


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost:27017/mass-flask-development-1',
        'tz_aware': True
    }

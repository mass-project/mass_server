from mass_server.config.config_base import BaseConfig


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost:27017/mass-flask-development',
        'tz_aware': True
    }

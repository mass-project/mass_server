from mass_server.config.config_base import BaseConfig


class ProductionConfig(BaseConfig):
    DEBUG = False
    MONGODB_SETTINGS = {
        'db': 'mass-flask-production',
        'host': 'localhost',
        'port': 27017,
        'tz_aware': True
    }

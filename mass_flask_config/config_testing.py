from mass_flask_config.config_base import BaseConfig


class TestingConfig(BaseConfig):
    TESTING = True
    MONGODB_SETTINGS = {
        'db': 'mass-flask-testing',
        'host': 'localhost',
        'port': 27017,
        'tz_aware': True
    }

from mass_flask_config.config_base import BaseConfig


class TestingConfig(BaseConfig):
    MASS_TESTING = True
    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost:27017/mass-flask-testing',
        'tz_aware': True
    }

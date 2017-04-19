from mass_server.config.config_base import BaseConfig


class TestingConfig(BaseConfig):
    TESTING = True
    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost:27017/mass-flask-testing',
        'tz_aware': True
    }

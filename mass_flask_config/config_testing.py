from mass_flask_config.config_base import BaseConfig


class TestingConfig(BaseConfig):
    MASS_TESTING = True
    MONGODB_SETTINGS = {
        'db': 'mass-flask-testing',
        'host': 'mongodb://localhost:27017/'
    }

from mass_flask_config.config_base import BaseConfig


class ProductionConfig(BaseConfig):
    DEBUG = False
    MONGODB_SETTINGS = {
        'db': 'mass-flask-production',
        'host': 'localhost',
        'port': 27017,
        'username': 'mass',
        'password': 'massdevdeploymentsecurepassword',
        'tz_aware': True
    }

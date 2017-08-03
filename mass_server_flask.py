from mass_flask_config.bootstrap import bootstrap_mass_flask
from mass_flask_config.app import app
from mass_flask_config.migration import schema_migration

bootstrap_mass_flask()
schema_migration()

if __name__ == '__main__':
    app.run()

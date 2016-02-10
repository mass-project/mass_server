from mass_flask_config.bootstrap import bootstrap_mass_flask
from mass_flask_config.app import app

bootstrap_mass_flask()

if __name__ == '__main__':
    app.run()

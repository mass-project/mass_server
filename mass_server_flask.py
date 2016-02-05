from mass_flask_config import app
from mass_flask_config.bootstrap import bootstrap_mass_flask

bootstrap_mass_flask()

if __name__ == '__main__':
    app.run()

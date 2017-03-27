from mass_server.config.bootstrap import bootstrap_mass_flask
from mass_server.config.app import app

bootstrap_mass_flask()

if __name__ == '__main__':
    app.run()

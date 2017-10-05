import os
from mass_server import get_production_app

app = get_production_app(os.getcwd())

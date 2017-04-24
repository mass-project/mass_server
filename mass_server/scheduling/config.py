import os

from flask import Blueprint
from flask_apscheduler import APScheduler
from uwsgi import worker_id


scheduling_blueprint = Blueprint('scheduling', __name__, template_folder='templates', static_folder='static')
scheduler = APScheduler()


@scheduling_blueprint.record_once
def on_load(state):
    if 'TESTING' in state.app.config and state.app.config['TESTING'] is True:
        print('Not starting scheduler when TESTING=True')
        return
    elif worker_id() == 1 and (not state.app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true'):
        from mass_server.scheduling.tasks import schedule_analyses
        scheduler.init_app(state.app)
        scheduler.add_job('schedule_analyses', schedule_analyses, trigger='interval', seconds=state.app.config['SCHEDULE_ANALYSES_INTERVAL'])
        scheduler.start()

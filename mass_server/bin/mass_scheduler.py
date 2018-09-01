import time
import logging
import signal
import sys

from datetime import datetime

import mass_server.queue.queue_context as queue_context
from mass_server import get_app
from mass_server.core.models import AnalysisRequest, AnalysisSystem
from mass_server.queue.utils import enqueue_analysis_request

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

app = get_app(set_server_name=True)
queue_connection = queue_context.connection
queue_channel = queue_context.channel


def schedule_analyses():
    logging.info('Scheduling...')
    with app.app_context():
        for system in AnalysisSystem.objects():
            queue_name = '{}_analysis-requests'.format(system.identifier_name)
            queue_context.ensure_queue(queue=queue_name, durable=True)

        due_analysis_requests = AnalysisRequest.objects().filter(schedule_after__lte=datetime.now(), enqueued=False)
        logging.info('Processing {} due analyses...'.format(len(due_analysis_requests)))

        for request in due_analysis_requests:
            enqueue_analysis_request(request)


def main():
    def shutdown(signum, frame):
        logging.warning('Shutting down. Closing queues and channels...')
        queue_context.shutdown()
        exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    while True:
        schedule_analyses()
        queue_context.connection.process_data_events()
        time.sleep(app.config['SCHEDULE_ANALYSES_INTERVAL'])


if __name__ == '__main__':
    main()

import time
import logging
import signal
from datetime import datetime

import mass_server.queue.queue_context as queue_context
from mass_server import get_app
from mass_server.core.models import AnalysisRequest, AnalysisSystem
from mass_server.queue.utils import enqueue_analysis_request

logging.getLogger(__name__).addHandler(logging.NullHandler())

app = get_app()
queue_context.start_connection(app.config['AMQP_URL'])
queue_connection = queue_context.connection
queue_channel = queue_context.channel


def schedule_analyses():
    logging.info('Scheduling...')
    with app.app_context():
        for system in AnalysisSystem.objects():
            queue_name = '{}_analysis-requests'.format(system.identifier_name)
            queue_channel.queue_declare(queue=queue_name, durable=True)

        due_analysis_requests = AnalysisRequest.objects().filter(schedule_after__lte=datetime.now(), enqueued=False)

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
        time.sleep(app.config['SCHEDULE_ANALYSES_INTERVAL'])


if __name__ == '__main__':
    main()

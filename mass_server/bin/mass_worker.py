from mass_server import get_app
from mass_server.queue import queue_context
from mass_server.core.models import AnalysisSystem, AnalysisRequest, Report
from mass_server.api.schemas import ReportSchema

from base64 import b64decode

import json
import logging
import signal
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

logging.getLogger(__name__).addHandler(logging.NullHandler())
app = get_app()
queue_context.start_connection(app.config['AMQP_URL'])
queue_connection = queue_context.connection
queue_channel = queue_context.channel

system_report_queues = {}


def report_callback(ch, method, properties, body):
    analysis_system = system_report_queues[method.routing_key]
    try:
        analysis_request = AnalysisRequest.objects.get(id=properties.headers['analysis_request'])
    except AnalysisRequest.DoesNotExist:
        logging.warning('Analysis Request does not exist.')
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    logging.debug('Processing report for {} on {}'.format(analysis_request, analysis_system))

    if analysis_request.analysis_system != analysis_system:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        raise ValueError('Mismatch between analysis request and analysis system.')

    data = json.loads(body)
    parsed_report = ReportSchema().load(data['report'], partial=True)
    report = parsed_report.data
    report.status = data['report']['status']

    report.sample = analysis_request.sample
    report.analysis_system = analysis_request.analysis_system

    if 'json_report_objects' in data and data['json_report_objects']:
        for k, v in data['json_report_objects'].items():
            report.add_json_report_object(json.dumps(v).encode('utf-8'), k)

    if 'raw_report_objects' in data and data['raw_report_objects']:
        for k, v in data['raw_report_objects'].items():
            report.add_raw_report_object(b64decode(v), k)

    report.save()

    if report.status == Report.REPORT_STATUS_CODE_FAILURE:
        analysis_request.increment_failure()
    else:
        analysis_request.delete()

    ch.basic_ack(delivery_tag=method.delivery_tag)


def command_callback(ch, method, properties, body):
    print(" [{}] {}".format(method.routing_key, body))


def initialize_queues_for_system(channel, system):
    report_queue = '{}_reports'.format(system.identifier_name)
    channel.queue_declare(queue=report_queue, durable=True)
    system_report_queues[report_queue] = system
    channel.basic_consume(report_callback, queue=report_queue, no_ack=False)


def main():
    logging.info('Starting worker. Connecting to queue server...')

    # Receive service commands
    queue_channel.exchange_declare(exchange='service_announcements',
                             exchange_type='fanout')
    service_queue = queue_channel.queue_declare(exclusive=True)
    queue_channel.queue_bind(exchange='service_announcements', queue=service_queue.method.queue)
    queue_channel.basic_consume(command_callback, service_queue.method.queue, no_ack=True)

    def shutdown(signum, frame):
        logging.warning('Shutting down. Closing queues and channels...')
        queue_context.shutdown()
        exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    for system in AnalysisSystem.objects:
        initialize_queues_for_system(queue_channel, system)

    queue_channel.start_consuming()


if __name__ == '__main__':
    main()

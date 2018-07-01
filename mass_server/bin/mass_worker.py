from mass_server import get_app
from mass_server.queue import queue_context
from mass_server.core.models import AnalysisRequest
from mass_server.api.schemas import ReportSchema, SampleRelationSchema

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


def report_callback(ch, method, properties, body):
    # TODO: Check api key
    logging.debug('Processing report for {}'.format(properties.headers['analysis_request']))

    data = json.loads(body)
    parsed_report = ReportSchema().load(data['data'], partial=True)
    report = parsed_report.data

    try:
        report.post_deserialization(analysis_request_id=properties.headers['analysis_request'], data=data['data'])
    except AnalysisRequest.DoesNotExist:
        logging.warning('Analysis Request does not exist.')
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    if 'additional_json_files' in data and data['additional_json_files']:
        for k, v in data['additional_json_files'].items():
            report.add_json_report_object(json.dumps(v).encode('utf-8'), k)

    if 'additional_binary_files' in data and data['additional_binary_files']:
        for k, v in data['additional_binary_files'].items():
            report.add_raw_report_object(b64decode(v), k)

    report.save()
    ch.basic_ack(delivery_tag=method.delivery_tag)


def sample_relation_callback(ch, method, properties, body):
    # TODO: Check api key
    logging.debug('Processing sample relation')

    data = json.loads(body)

    with app.app_context():
        parsed_relation = SampleRelationSchema().load(data['data'])

    if parsed_relation.errors:
        raise ValueError(parsed_relation.errors)

    relation = parsed_relation.data
    relation.save()

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    logging.info('Starting worker. Connecting to queue server...')

    queue_channel.queue_declare(queue='reports', durable=True)
    queue_channel.queue_declare(queue='sample_relations', durable=True)
    queue_channel.basic_consume(report_callback, queue='reports', no_ack=False)
    queue_channel.basic_consume(sample_relation_callback, queue='sample_relations', no_ack=False)

    def shutdown(signum, frame):
        logging.warning('Shutting down. Closing queues and channels...')
        queue_context.shutdown()
        exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    queue_channel.start_consuming()


if __name__ == '__main__':
    main()

from mass_server import get_app
from mass_server.queue import queue_context
from mass_server.core.models import AnalysisRequest, Sample, AnalysisSystem
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
app = get_app(set_server_name=True)
queue_context.start_connection(app.config['AMQP_URL'])
queue_connection = queue_context.connection
queue_channel = queue_context.channel


def load_object_wrapper(schema, partial=False):
    # TODO: Check api key
    def real_decorator(func):
        def wrapper(ch, method, properties, body):
            data = json.loads(body)

            with app.app_context():
                parsed = schema.load(data['data'], partial=partial)

                if parsed.errors:
                    raise ValueError(parsed.errors)

                return func(ch, method, properties, data, parsed.data)

        return wrapper
    return real_decorator


def catch_exception(exception, ack=False, message=None):
    if not message:
        message = ''

    def real_decorator(func):
        def wrapper(ch, method, properties, body):
            try:
                func(ch, method, properties, body)
            except exception:
                logging.warning(message)
                if ack:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
        return wrapper
    return real_decorator


@catch_exception(AnalysisRequest.DoesNotExist, ack=True, message='Analysis Request does not exist.')
@catch_exception(Sample.DoesNotExist, ack=True, message='Sample does not exist.')
@catch_exception(AnalysisSystem.DoesNotExist, ack=True, message='AnalysisSystem does not exist.')
@load_object_wrapper(ReportSchema(), partial=True)
def report_callback(ch, method, properties, data, report):

    if 'analysis_request' in properties.headers:
        request_id = properties.headers['analysis_request']
        logging.debug('Processing report for analysis request {}'.format(request_id))
    else:
        request_id = None
        logging.debug('Processing report for {} on {}'.format(report.sample, report.analysis_system))

    report.post_deserialization(data=data['data'], analysis_request_id=request_id)

    if 'additional_json_files' in data and data['additional_json_files']:
        for k, v in data['additional_json_files'].items():
            report.add_json_report_object(json.dumps(v).encode('utf-8'), k)

    if 'additional_binary_files' in data and data['additional_binary_files']:
        for k, v in data['additional_binary_files'].items():
            report.add_raw_report_object(b64decode(v), k)

    report.save()

    ch.basic_ack(delivery_tag=method.delivery_tag)


def sample_callback(ch, method, properties, body):
    logging.debug('Creating sample')

    data = json.loads(body)['data']
    if not 'unique_features' in data:
        data['unique_features'] = {}

    if 'additional_binary_files' in data and data['additional_binary_files']:
        data['unique_features']['file'] = b64decode(data['additional_binary_files']['file'])

    with app.app_context():
        Sample.create_or_update(**data)
    ch.basic_ack(delivery_tag=method.delivery_tag)


@load_object_wrapper(SampleRelationSchema())
def sample_relation_callback(ch, method, properties, data, relation):
    logging.debug('Processing sample relation')
    relation.save()
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    logging.info('Starting worker. Connecting to queue server...')

    queue_channel.queue_declare(queue='reports', durable=True)
    queue_channel.queue_declare(queue='samples', durable=True)
    queue_channel.queue_declare(queue='sample_relations', durable=True)
    queue_channel.basic_consume(report_callback, queue='reports', no_ack=False)
    queue_channel.basic_consume(sample_callback, queue='samples', no_ack=False)
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

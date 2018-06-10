from pika import BlockingConnection, URLParameters

from mass_server import get_app

import logging
import signal

app = get_app()
logging.getLogger(__name__).addHandler(logging.NullHandler())


def report_callback(ch, method, properties, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    logging.info('Starting worker. Connecting to queue server...')
    connection = BlockingConnection(URLParameters(app.config['AMQP_URL']))
    channel = connection.channel()
    channel.queue_declare(queue='reports')

    def shutdown(signum, frame):
        logging.warning('Shutting down. Closing queues and channels...')
        connection.close()
        exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    channel.basic_consume(report_callback, queue='reports', no_ack=False)
    channel.start_consuming()


if __name__ == '__main__':
    main()

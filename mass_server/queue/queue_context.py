from pika import BlockingConnection, URLParameters
from pika.exceptions import ConnectionClosed

connection = None
channel = None
created_queues = set()
_connection_parameters = None


def start_connection(amqp_url):
    global connection, channel, _connection_parameters
    _connection_parameters = URLParameters(amqp_url)
    connection = BlockingConnection(_connection_parameters)
    channel = connection.channel()


def ensure_connection():
    global connection, channel
    try:
        connection.process_data_events()
    except (ConnectionClosed, AttributeError):
        connection = BlockingConnection(_connection_parameters)
        channel = connection.channel()


def ensure_queue(queue, durable):
    if queue not in created_queues:
        channel.queue_declare(queue=queue, durable=durable)
        created_queues.add(queue)


def shutdown():
    connection.close()

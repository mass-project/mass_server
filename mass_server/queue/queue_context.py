from pika import BlockingConnection, URLParameters

connection = None
channel = None
created_queues = set()


def start_connection(amqp_url):
    global connection, channel
    connection = BlockingConnection(URLParameters(amqp_url))
    channel = connection.channel()


def ensure_queue(queue, durable):
    if queue not in created_queues:
        channel.queue_declare(queue=queue, durable=durable)
        created_queues.add(queue)


def shutdown():
    connection.close()

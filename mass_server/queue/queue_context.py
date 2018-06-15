from pika import BlockingConnection, URLParameters

connection = None
channel = None


def start_connection(amqp_url):
    global connection, channel
    connection = BlockingConnection(URLParameters(amqp_url))
    channel = connection.channel()


def shutdown():
    connection.close()

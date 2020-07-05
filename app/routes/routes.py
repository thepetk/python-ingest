import socket
import json
import sys
import threading

from collections import namedtuple
from time import sleep

from app import app, db
from app.models.event import Event
from .routes_utils import create_session
from .publisher import Publisher


# Set up Global Variables:
host = app.config['INGEST_HOST']
port = int(app.config['INGEST_PORT'])

# Settings for RabbitMQ Publisher object
publisher_conf_dict = {
    'username': str(app.config['RMQ_USERNAME']),
    'password': str(app.config['RMQ_PASSWORD']),
    'host': str(app.config['RMQ_HOST']),
    'port': str(app.config['RMQ_PORT']),
    'routingKey':str(app.config['RMQ_QUEUE'])
}


def service_connection(thread_data):
    '''
    Handles thread data from ingest loop.
    '''
    # Parse connection and address from thread data
    gwConnection, gwAddress = thread_data
    app.logger.info('Received from:%s' % str(gwAddress))

    # Fetch data from connection, notify for success and close connection
    recv_data = gwConnection.recv(2048)
    response= b'1'
    gwConnection.send(response)
    gwConnection.close()

    # No recv_data means empty socket body
    if recv_data:
        # Decode received data with utf-8 and converse string to immutable type - namedtuple
        decoded_data = recv_data.decode('utf-8')
        # TODO - This step is optional. You may want to proceed with dict type
        decoded_event = json.loads(decoded_data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

        # Create new event on database. Multiple available ways to save event. We just wanted a verbose and
        # easy-to-understand way.
        event = Event(
            device_number = decoded_event.device_number,
            event_code = decoded_event.event_code,
            message_date = decoded_event.message_date,
            longitude = decoded_event.longitude,
            latitude = decoded_event.latitude)
        try:
            db_session = create_session()
            db_session.merge(event)
            db_session.commit()

            # Too many open PostgreSQL connections may give you an error
            db_session.close()
            app.logger.info('Event %s Pushed Successfully to PostgreSQL' % (str(gwAddress)))
        except Exception as e:
            # TODO - Here you can add different actions according to type of error.
            # Most common case, PostgreSQL is down. You may have, for example, to restart it

            # Our action: Upon save failure publish to rabbitmq
            publisher = Publisher()
            publisher.init(publisher_conf_dict)
            publisher.publish(decoded_data)
            app.logger.info('Error: %s' % (str(e)))
            app.logger.info('Event Published to RabbitMQ through Publisher')
    else:
        app.logger.warning('Socket empty. Connection closed')


def parse_sockets():
    """
    The main function of python-ingest
    """

    threads_list = []

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as gw_socket:
        try:
            gw_socket.bind((host, port))
        except OSError:
            # If address is used from previous instance sleep for some seconds and retry
            app.logger.warning('Address in use from previous instance. Reconnecting in %s seconds..' % (
                                                                    str(app.config['RECONNECT_TIMEOUT'])))
            sleep(int(app.config['RECONNECT_TIMEOUT']))
            parse_sockets()

        gw_socket.listen()
        app.logger.info('Listening to: %s:%s' % (str(host), str(port)))

        while True:
            try:
                # When a new socket comes create a new thread.
                # TODO - Best practice here to use a ThreadPoolExecutor. With this technique you can use already created
                # inactive threads.
                new_thread = threading.Thread(target=service_connection, args=(gw_socket.accept(),)).start()
                threads_list.append(new_thread)

            except KeyboardInterrupt:
                # Close all open threads after cntrl+C
                app.logger.info('Closing all threads..')
                for thread in threads_list:
                    if thread:
                        thread.join()
                app.logger.info('Closing Ingest. Bye')
                sys.exit()

            except RuntimeError as e:
                app.logger.warning('Runtime Error: %' % (str(e)))

# Run parse socket method. This could be done also with a manage.py or from __init__.py file or something else
parse_sockets()
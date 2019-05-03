# -*- coding: utf-8 -*-
import click
import json
import logging.config
import sys
import simplejson as json
import paho.mqtt.client
import zmq
from .config import load_config

__version__ = '@@VERSION@@'


@click.command()
@click.option('--config', '-c', 'config_file', type=click.File('r'), required=True, help='Configuration file.')
@click.option('--test', is_flag=True, help='Test configuration file.')
@click.version_option(version=__version__)
def cli(config_file, test=False):
    '''ZeroMQ to Azure IoT Hub.'''

    try:
        config = load_config(config_file)
        config_file.close()
    except Exception as e:
        logging.error('Failed opening configuration file')
        logging.error(str(e))
        sys.exit(1)

    if test:
        click.echo("The configuration file seems ok")
        return

    logging.config.dictConfig(config['log'])
    logging.info('Process started')

    run(config)


def run(config):

    context = zmq.Context()
    sock = context.socket(zmq.SUB)
    sock.setsockopt_string(zmq.SUBSCRIBE, '')
    sock.connect('tcp://%s:%d' % (config['zmq']['host'], config['zmq']['port']))

    cmqtt = paho.mqtt.client.Client()

    if config['mqtt'].get('username', None):
        cmqtt.username_pw_set(config['mqtt']['username'],
                              config['mqtt'].get('password', None))

    if config['mqtt'].get('cafile', None):
        cmqtt.tls_set(config['mqtt']['cafile'],
                      config['mqtt'].get('certfile', None),
                      config['mqtt'].get('keyfile', None))

    cmqtt.on_connect = _on_mqtt_connect
    cmqtt.on_disconnect = _on_mqtt_disconnect

    logging.info('MQTT broker host: %s, port: %d, use tls: %s',
                 config['mqtt']['host'],
                 config['mqtt']['port'],
                 bool(config['mqtt'].get('cafile', None)))

    cmqtt.connect_async(config['mqtt']['host'], config['mqtt']['port'], keepalive=10)
    cmqtt.loop_start()

    strip_key = config['mqtt'].get('strip', None)

    while True:
        try:
            payload = sock.recv_json()
            logging.debug("Recv %s", payload)
            topic = config['mqtt']['topic']
            topic = topic.replace("$id", payload['id'])
            topic = topic.replace("$type", payload['type'])

            if strip_key:
                for key in strip_key:
                    payload.pop(key, None)

            cmqtt.publish(topic, json.dumps(payload, use_decimal=True))
        except Exception:
            logging.error('Unhandled exception', exc_info=True)


def _on_mqtt_connect(client, userdata, flags, rc):
    logging.info('Connected to MQTT broker with code %s', rc)

    lut = {paho.mqtt.client.CONNACK_REFUSED_PROTOCOL_VERSION: 'incorrect protocol version',
           paho.mqtt.client.CONNACK_REFUSED_IDENTIFIER_REJECTED: 'invalid client identifier',
           paho.mqtt.client.CONNACK_REFUSED_SERVER_UNAVAILABLE: 'server unavailable',
           paho.mqtt.client.CONNACK_REFUSED_BAD_USERNAME_PASSWORD: 'bad username or password',
           paho.mqtt.client.CONNACK_REFUSED_NOT_AUTHORIZED: 'not authorised'}

    if rc != paho.mqtt.client.CONNACK_ACCEPTED:
        logging.error('Connection refused from reason: %s', lut.get(rc, 'unknown code'))


def _on_mqtt_disconnect(client, userdata, rc):
    logging.info('Disconnect from MQTT broker with code %s', rc)


def main():
    try:
        cli()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        click.echo(str(e), err=True)
        sys.exit(1)

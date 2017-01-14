import AWSIoTPythonSDK
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import alexi.gps_reader as gps
import alexi.server as server

from alexi.iot.config import (ENDPOINT, PORT, CLIENT_ID,
                              ROOT_CERTIFICATE_FILE, CERTIFICATE_FILE, PRIVATE_KEY_FILE)


# Global client used for MQTT
_client = None
_shutdown = lambda: None

class Topic(object):
    @staticmethod
    def get_name():
        raise NotImplementedError()

    @staticmethod
    def callback():
        raise NotImplementedError()

class NavigateTo(Topic):
    @staticmethod
    def get_name():
        return "/pi-nav/navigate-to"

    @staticmethod
    def callback(client, userdata, message):
        print "Got request to navigate-to: {}".format(message.payload)
        payload = json.loads(message.payload)
        server.enqueue_action("navigate-to", payload)

class Shutdown(Topic):
    @staticmethod
    def get_name():
        return "/pi-nav/shutdown"

    @staticmethod
    def callback(client, userdata, message):
        print "Got request to shut down!"
        _shutdown(switch_off=True)


def start(on_shutdown=_shutdown):
    global _client
    global _shutdown

    _shutdown = on_shutdown

    if _client is not None:
        stop()

    _client = AWSIoTMQTTClient(CLIENT_ID)
    _client.configureEndpoint(ENDPOINT, PORT)
    _client.configureCredentials(ROOT_CERTIFICATE_FILE, PRIVATE_KEY_FILE, CERTIFICATE_FILE)

    # Keep up to 20 offline requests - drop old ones
    _client.configureOfflinePublishQueueing(20, AWSIoTPythonSDK.MQTTLib.DROP_OLDEST)
    _client.configureDrainingFrequency(2)  # Draining: 2 Hz
    _client.configureConnectDisconnectTimeout(10)  # 10 sec
    _client.configureMQTTOperationTimeout(5)  # 5 sec

    _client.connect()

    # Subscribe to all the topics
    for topic in Topic.__subclasses__():
        _client.subscribe(topic.get_name(), 1, topic.callback)


def stop():
    global _client
    global _shutdown
    _shutdown = lambda: None
    # Unsubscribe from everything and disconnect
    # for topic in Topic.__subclasses__():
    #     _client.unsubscribe(topic.get_name())
    # _client.disconnect()



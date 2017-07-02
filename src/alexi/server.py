from threading import Thread
from flask import Flask
import json
import os
from Queue import Queue
from flask_socketio import SocketIO

_action_queue = Queue()

app = Flask(__name__, static_url_path='', static_folder='/home/pi/pi-nav/static')
sio = SocketIO(app, logger=True, async_mode='eventlet', engineio_logger=True)

@app.route('/')
def root():
    print "Hitting root of the site!"
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)

@sio.on('connect')
def connect():
    print "Something connected!"


@sio.on('jack')
def jack(data):
    print "Got a jack!"
    print data
    sio.emit('squirrel', data);


@sio.on_error()
def on_error(err):
    print "Socket error"
    print err


def _emit(name, data):
    global sio
    #print "{} emitted with data: {}".format(name, data)
    sio.emit(name, data)

def send_gps(data):
    _emit('gps-update', data)


def enqueue_action(name, payload):
    _emit(name, payload)


def send_ecu_update(data):
    _emit('ecu-update', data)


class Server(Thread):
    def __init__(self, port=5555):
        Thread.__init__(self)
        self.port = port

    def run(self):
        global app
        global sio
        sio.run(app, port=self.port)

    def stop(self):
        pass

_server = None


def start(port=5555):
    global _server

    if _server is not None:
        _server.stop()

    _server = Server(port=port)
    _server.start()


def stop():
    global _server
    _server.stop()
    _server = None

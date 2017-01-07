from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

import alexi.gps_reader as gps
import json

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        response = '{}'

        if self.path == '/api/gps':
            response = json.dumps(gps.get_data())

        self._set_headers()
        self.wfile.write(response)

    def do_HEAD(self):
        self._set_headers()


class Server(Thread):
    def __init__(self, port=5555):
        Thread.__init__(self)
        self.port = port
        self.active = True

    def run(self):
        self._httpd = HTTPServer(('', self.port), Handler)

        while self.active:
            self._httpd.handle_request()

        self._httpd.server_close()

    def stop(self):
        self.active = False


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
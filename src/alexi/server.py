from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from threading import Thread

import alexi.gps_reader as gps
import json
import os

class Handler(SimpleHTTPRequestHandler):
    def _set_api_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/gps':
            response = json.dumps(gps.get_data())
            self._set_api_headers()
            self.wfile.write(response)
            return

        # Fall back to serving the static folder
        current_dir = os.getcwd()
        os.chdir('static')
        SimpleHTTPRequestHandler.do_GET(self)
        os.chdir(current_dir)


class Server(Thread):
    def __init__(self, port=5555):
        Thread.__init__(self)
        self.port = port
        self.active = True

    def run(self):
        self._httpd = HTTPServer(('', self.port), Handler)

        while self.active:
            self._httpd.handle_request()


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
import os
import logging
import struct
import socket
import json

import tornado.ioloop
import tornado.web
import tornado.websocket

# REQUIRES TORNADO MODULE
from tornado.options import define, options

log = logging.getLogger(__name__)
WEBSOCKS = []

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/static/maps.html")


class WebSocketBroadcaster(tornado.websocket.WebSocketHandler):
    """Keeps track of all websocket connections in
    the global WEBSOCKS variable.
    
    """
    def __init__(self, *args, **kwargs):
        super(WebSocketBroadcaster, self).__init__(*args, **kwargs)

    def open(self):
        log.info("Opened socket %r" % self)
        global WEBSOCKS
        WEBSOCKS.append(self)

    # Handles a message from the web application
    def on_message(self, message):
        # Converts incoming message to a python dictionary from JSON
        request_info = json.loads(message)
        print 'Received request for: ' + str(request_info)
        

    def on_close(self):
        log.info("Closed socket %r" % self)
        global WEBSOCKS
        WEBSOCKS.remove(self)

    def check_origin(self, origin):
        return True

settings = {
    'static_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), ""),
}
print settings

application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/sock", WebSocketBroadcaster)
        ],
    **settings)


if __name__ == "__main__":
    define("port", default=8000, help="Run server on a specific port", type=int)
    tornado.options.parse_command_line()

    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
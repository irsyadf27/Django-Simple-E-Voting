import datetime
import json
import time
import urllib

import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.httpclient

from django.conf import settings
from importlib import import_module
from django.contrib.auth.models import User

SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

clients = []

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/plain')
        self.write('Hello. :)')

class MessagesHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(MessagesHandler, self).__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    def open(self):
        session_key = self.get_cookie(settings.SESSION_COOKIE_NAME)
        session = SessionStore(session_key=session_key)
        if session.get('_auth_user_id') is None:
            self.close()

    def on_message(self, message):
        message = json.loads(message)
        if message.get('type') == "admin":
            clients.append(self)
        else:
            # kirim ke admin
            for client in clients:
                client.write_message(json.dumps(message))
                
    def on_close(self):
        if self in clients:
            clients.remove(self)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/vote", MessagesHandler),
], debug=True)
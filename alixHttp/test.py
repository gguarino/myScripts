#!/usr/bin/env python
import logging, os, sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options, parse_command_line, parse_config_file
from ws.mountHandler import mountHandler
from ws.usbHandler import usbHandler
from ws.daemonHandler import daemonHandler


daemon_directory=os.path.dirname(__file__)
define('config_file', default=daemon_directory+'/alix.cfg', help='filename for additional configuration')
define('app_name', default='app-name', type=str)
define("port", default=8888, help="run on the given port", type=int)
define("serv", default=[], help="", type=list)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"(.*)",MainHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html", options=options)
    def get_error_html(self, status_code, **kwargs):
        self.write("<html><body><h1>404!</h1></body></html>")

def main():

    tornado.options.parse_command_line()
    parse_config_file(options.config_file)
    print options.serv[0]

if __name__ == "__main__":
    main()
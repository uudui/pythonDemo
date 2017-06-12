#!/usr/bin/env python

# -*- coding: utf-8 -*-
import logging
import os.path
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from celery import Celery
import tcelery,task

log = logging.getLogger('demo')

define("port", default=8003, help="run on the given port", type=int)
tcelery.setup_nonblocking_producer()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
            (r'/query', QueryHandler),
            (r"/sleep", SleepHandler),
            (r"/justnow", JustNowHandler)
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            xsrf_cookies=True,
            login_url="/login",
            debug=True,
        )

        tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html", user=self.current_user)

class QueryHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        query_drivers = self.get_argument("drivers")
        order = self.get_argument("order")
        driver = self.get_argument("driver")




class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.get_argument("username")
        self.set_secure_cookie("username", username)
        self.redirect("/")


class LogoutHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.clear_cookie("username")
            self.redirect("/")

tcelery.setup_nonblocking_producer()

class SleepHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        #task.sleep.apply_async(args=[5])
        yield tornado.gen.Task(task.sleep.apply_async, args=[5])
        self.write("when i sleep 5s")
        self.finish()

class JustNowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("i hope just now see you")


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

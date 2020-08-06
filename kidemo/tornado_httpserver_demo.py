# -*- coding: utf-8 -*-
# author: kuangdd
# date: 2020/8/6
"""
### Tornado服务部署
tornado_httpserver_demo

* 怎样部署Tornado的web服务或接口。
* GET和POST方法的构建方法。
"""
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(Path(__name__).stem)

import json
from tornado.web import Application, RequestHandler, url
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import options, define


class IndexHandler(RequestHandler):
    def get(self):
        self.write("<a href='" + self.reverse_url("login") + "'>登录</a>")


class RegistHandler(RequestHandler):
    def initialize(self, **kwargs):
        self.kwargs = json.dumps(kwargs, ensure_ascii=False)

    def get(self):
        self.write("注册: {}".format(self.kwargs))


class LoginHandler(RequestHandler):
    def get(self):
        self.write("登录页面")

    def post(self):
        self.write("登录处理")


def run_server():
    define("port", default=8000, type=int)
    define("address", default="0.0.0.0", type=str)
    define("subdomain", default="/index", type=str)

    app = Application(
        [
            (options.subdomain, IndexHandler),
            ("/regist", RegistHandler, {"name": "注册"}),
            url("/login", LoginHandler, name="login"),
        ]
    )

    http_server = HTTPServer(app)
    http_server.listen(port=options.port, address=options.address)

    IOLoop.current().start()


if __name__ == "__main__":
    print(__file__)
    run_server()

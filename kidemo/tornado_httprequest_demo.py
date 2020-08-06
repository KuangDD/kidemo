# -*- coding: utf-8 -*-
# author: kuangdd
# date: 2020/8/4
"""
### Tornado异步访问
tornado_httprequest_demo

* Tornado怎么访问web接口。
* Tornado怎么获取接口返回的数据。
* 怎样获取到异步返回的数据。
* 用callback的方式处理Tornado返回的数据。
* 用常规方式处理Tornado返回的数据。
"""
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(Path(__name__).stem)

from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
from tornado.httpclient import HTTPClient
import tornado.ioloop
import asyncio
import nest_asyncio

# 修正“RuntimeError: This event loop is already running”的报错。
nest_asyncio.apply()

_url = 'https://www.baidu.com/'


def get_sync(url=_url):
    """同步"""
    request = HTTPRequest(url=url, method='GET')
    http_client = HTTPClient()
    response = http_client.fetch(request)
    return response


def run_get_sync():
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(get_async()) for _ in range(10)]
    loop.run_until_complete(asyncio.wait(tasks))

    # 多个loop执行则不用close。
    # loop.close()
    print(get_sync.__doc__, get_sync.__name__)
    for task in tasks:
        out = task.result()
        print(out)


async def get_async(url=_url):
    """异步"""
    request = HTTPRequest(url=url, method='GET')
    http_client = AsyncHTTPClient()
    return await http_client.fetch(request)


def run_get_async():
    loop = asyncio.get_event_loop()
    tasks = []
    for _ in range(10):
        task = loop.create_task(get_async())
        loop.run_until_complete(task)
        tasks.append(task)

    print(get_async.__doc__, get_async.__name__)
    for task in tasks:
        out = task.result()
        print(out)


def get_async_callback(url=_url, callback=None):
    """异步（用callback处理结果）"""
    request = HTTPRequest(url=url, method='GET')
    http_client = AsyncHTTPClient()
    http_client.fetch(request, callback)


def callback_func(response):
    if response.error:
        print(get_async.__doc__, get_sync.__name__)
        print(response)
    else:
        print(get_async_callback.__doc__, get_async_callback.__name__)
        print(response)


def run_get_async_callback():
    for _ in range(10):
        get_async_callback(callback=callback_func)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    print(__file__)
    run_get_sync()
    run_get_async()
    run_get_async_callback()

# -*- coding: utf-8 -*-
# author: kuangdd
# date: 2020/8/5
"""
### 异步编程
async_demo

* 异步函数的写法。
* 异步函数怎么执行。
* 异步函数怎么获取返回的结果。
"""
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(Path(__name__).stem)

import json
import asyncio


async def func_async(*args, **kwargs):
    """异步函数"""
    await asyncio.sleep(1.)
    out = json.dumps(kwargs)
    return out


def run_func_async():
    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(10):
        task = loop.create_task(func_async(num=i))
        tasks.append(task)

    loop.run_until_complete(asyncio.wait(tasks))

    outs = []
    for task in tasks:
        out = task.result()
        outs.append(out)

    print(func_async.__doc__, func_async.__name__)
    for out in outs:
        print(out)
    return outs


if __name__ == "__main__":
    print(__file__)
    run_func_async()

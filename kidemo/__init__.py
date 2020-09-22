# -*- coding: utf-8 -*-
# author: kuangdd
# date: 2020/8/6
"""
## kidemo
kid demo,像小孩学习一样的demo。

### 数据资源
关注微信公众号【啊啦嘻哈】，回复【kidemo】获取以下资源。

![啊啦嘻哈](fig/alaxiha.png)

* 文字格式ttf文件，全部为免费商用字体。
* markdown主题渲染的css文件。
* 幽默笑话汇总。
"""
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(Path(__name__).stem)

if __name__ == "__main__":
    print(__file__)

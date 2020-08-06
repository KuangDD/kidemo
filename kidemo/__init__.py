# -*- coding: utf-8 -*-
# author: kuangdd
# date: 2020/8/6
"""
## kidemo
kid demo,像小孩学习一样的demo。
"""
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(Path(__name__).stem)

if __name__ == "__main__":
    print(__file__)

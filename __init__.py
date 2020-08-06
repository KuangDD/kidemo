# -*- coding: utf-8 -*-
# author: kuangdd
# date: 2020/8/6
"""
__init__
"""
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(Path(__name__).stem)


def create_readme():
    import kidemo
    from kidemo import async_demo, tornado_httprequest_demo, tornado_httpserver_demo
    readme_docs = [kidemo.__doc__,
                   async_demo.__doc__,
                   tornado_httprequest_demo.__doc__,
                   tornado_httpserver_demo.__doc__]
    with open("README.md", "wt", encoding="utf8") as fout:
        for doc in readme_docs:
            fout.write(doc)
    return "".join(readme_docs)


if __name__ == "__main__":
    print(__file__)
    create_readme()

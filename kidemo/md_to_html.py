# -*- coding: utf-8 -*-
# author: kuangdd
# date: 2020/9/21
"""
### markdown格式文本转为html
md_to_html

* 把markdown格式编辑的md文本渲染为html格式显示。
* 可以设置渲染html的风格CSS。
* 可以用命令行方式执行，说明如下：

```
usage: 把markdown格式文本转为html。

python md_to_html.py [-h] [-i INPUT] [-o OUTPUT] [-c CSS]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        需要转为html的md文件路径。
  -o OUTPUT, --output OUTPUT
                        保存html的路径。
  -c CSS, --css CSS     主题文件CSS路径。

```
"""
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(Path(__name__).stem)

import markdown
import os.path as op
from bs4 import BeautifulSoup


class Markdown2Html:
    def __init__(self, cssfile=None):
        '''
        初始化 Markdown2Html 类，可传入特定 css 文件作为样式
        '''
        self.headTag = '<head><meta charset="utf-8" /></head>'
        if cssfile:
            self.setStyle(cssfile)

    def setStyle(self, cssfile=None):
        '''
        设置样式表文件
        '''
        if cssfile is None:
            self.headTag = '<head><meta charset="utf-8" /></head>'
        else:
            try:
                with open(cssfile, 'r', encoding='utf8') as f:
                    css = f.read()
            except UnicodeDecodeError:
                with open(cssfile, 'r') as f:
                    css = f.read()
            self.headTag = self.headTag[:-7] \
                           + f'<style  type="text/css">{css}</style>' \
                           + self.headTag[-7:]

    def convert(self, infile, outfile=None, prettify=False):
        '''
        转换文件
        '''
        if not op.isfile(infile):
            print('请输入正确的 markdown 文件路径！')
            return

        if outfile is None:
            outfile = op.splitext(infile)[0] + '.html'
        try:
            with open(infile, 'r', encoding='utf8') as f:
                markdownText = f.read()
        except UnicodeDecodeError:
            with open(infile, 'r') as f:
                markdownText = f.read()

        rawhtml = self.headTag + markdown.markdown(
            markdownText, output_format='html5', extensions=['extra'])

        if prettify:
            prettyHtml = BeautifulSoup(rawhtml, 'html5lib').prettify()
            with open(outfile, 'w', encoding='utf8') as f:
                f.write(prettyHtml)
        else:
            with open(outfile, 'w', encoding='utf8') as f:
                f.write(rawhtml)


def parse_args():
    """命令行执行。"""
    import argparse
    parser = argparse.ArgumentParser('把markdown格式文本转为html。')

    parser.add_argument('-i', '--input', type=str, default='data/my_joke_003.md',
                        help='需要转为html的md文件路径。')
    parser.add_argument('-o', '--output', type=str, default='data/my_joke_003.html',
                        help='保存html的路径。')
    parser.add_argument('-c', '--css', type=str, default='theme/whitelines.css',
                        help='主题文件CSS路径。')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    m2h = Markdown2Html(args.css)
    m2h.convert(args.input, args.output)

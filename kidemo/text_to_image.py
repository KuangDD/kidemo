# -*- coding: utf-8 -*-
# author: kuangdd
# date: 2020/9/21
"""
### 文字转为图片
text_to_image

* 把文字转为图片，可以制作点阵文字。
* 可以设置文字类型和文字大小。
* 可以用命令行方式执行，说明如下：

```
usage: 把文本转为图片。

python text_to_image.py [-h] [-i INPUT] [-o OUTPUT] [-f FONT] [-s SIZE]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        需要转为图片的文字。
  -o OUTPUT, --output OUTPUT
                        保存图片的路径。
  -f FONT, --font FONT  文字类型文件路径。
  -s SIZE, --size SIZE  文字大小。
```
"""
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(Path(__name__).stem)

import pygame

_font_path = 'font/HYJunHei-85W.ttf'
pygame.init()  # 初始化


def text2image(text, outpath, font_path=_font_path, font_size=28):
    """把文字转为图片，图片像素点做点阵汉字。"""
    # 设置字体大小及路径
    font = pygame.font.Font(str(font_path), font_size)

    # 设置位置及颜色
    font_text = font.render(text, True, (0, 0, 0), (255, 255, 255))

    # 保存图片及路径
    pygame.image.save(font_text, outpath)


def parse_args():
    """命令行执行。"""
    import argparse
    parser = argparse.ArgumentParser('把文本转为图片。')

    parser.add_argument('-i', '--input', type=str, default=r'好',
                        help='需要转为图片的文字。')
    parser.add_argument('-o', '--output', type=str, default='data/hao.png',
                        help='保存图片的路径。')
    parser.add_argument('-f', '--font', type=str, default=_font_path,
                        help='文字类型文件路径。')
    parser.add_argument('-s', '--size', type=int, default=28,
                        help='文字大小。')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    text2image(text=args.input, outpath=args.output, font_path=args.font, font_size=args.size)

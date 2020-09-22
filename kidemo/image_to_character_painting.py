# -*- coding: utf-8 -*-
# author: kuangdd
# date: 2020/9/21
"""
### 图片转为字符画
image_to_character_painting

* 把图片转为字符画显示。
* 可以设置字符画的字符。
* 可以用命令行方式执行，说明如下：

```
usage: 把图片转为字符画。

python image_to_character_painting.py [-h] [-i INPUT] [-o OUTPUT] [-W WIDTH] [-H HEIGHT] [-t TABLE]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        需要转为字符画的图片路径。
  -o OUTPUT, --output OUTPUT
                        保存字符画的文本路径，如果为空则打印到屏幕。
  -W WIDTH, --width WIDTH
                        字符画的长度。
  -H HEIGHT, --height HEIGHT
                        字符画的高度。
  -t TABLE, --table TABLE
                        字符的列表。
```
"""
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(Path(__name__).stem)

from PIL import Image

# 半角转全角映射表
ban2quan_dict = {i: i + 65248 for i in range(33, 127)}
ban2quan_dict.update({32: 12288})

# 全角转半角映射表
quan2ban_dict = {v: k for k, v in ban2quan_dict.items()}


def ban2quan(text: str):
    """
    半角转全角
    :param text:
    :return:
    """
    return text.translate(ban2quan_dict)


def quan2ban(text: str):
    """
    全角转半角
    :param text:
    :return:
    """
    return text.translate(quan2ban_dict)


ascii_char = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.   "  # 设置显示的字符集
ascii_char_half = tuple([w + w for w in ascii_char])
ascii_char_full = tuple(list(ban2quan(ascii_char)))


def get_char(r, g, b, alpha=256, char_table=ascii_char_full):
    """将256灰度映射到char_table字符上。"""
    # alpha为透明度
    # 判断 alpha 值，为0表示全透明
    if alpha == 0:
        return char_table[-1]

    # 获取字符集的长度，这里为 70
    length = len(char_table)
    # 将 RGB 值转为灰度值 gray，灰度值范围为 0-255
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    # 灰度值范围为 0-255，而字符集只有 70
    # 需要进行如下处理才能将灰度值映射到指定的字符上
    # 防止当灰度值为255时，输出的第70个字符超出列表索引，所以需要将(255+1)
    unit = 255.0 / length

    # 返回灰度值对应的字符
    return char_table[min(len(char_table) - 1, int(gray / unit))]


def image2charaterpainting(image_path, out_size=(100, 100), char_table=ascii_char_full):
    # 打开并调整图片的宽和高

    im = Image.open(image_path)
    im = im.resize((out_size[0], out_size[1]), Image.NEAREST)

    # 初始化输出的字符串
    char_lst = []
    # 遍历图片中的每一行
    for i in range(out_size[1]):
        # 遍历该行中的每一列
        for j in range(out_size[0]):
            # 将 (j,i) 坐标的 RGB 像素转为字符后添加到 txt 字符串
            char_lst.append(get_char(*im.getpixel((j, i)), char_table=char_table))
            # txt += get_char(*im.getpixel((j, i)))
        # 遍历完一行后需要增加换行符
        char_lst.append('\n')
        # txt += '\n'
    txt = ''.join(char_lst)
    return txt


def save_txt(text, outpath=''):
    if not outpath:
        print(text)
    else:
        with open(outpath, 'w', encoding='utf8') as fout:
            fout.write(text)


def parse_args():
    """命令行执行。"""
    import argparse
    parser = argparse.ArgumentParser('把图片转为字符画。')

    parser.add_argument('-i', '--input', type=str, default='data/hao.png',
                        help='需要转为字符画的图片路径。')
    parser.add_argument('-o', '--output', type=str, default='data/hao.txt',
                        help='保存字符画的文本路径，如果为空则打印到屏幕。')
    parser.add_argument('-W', '--width', type=int, default=28,
                        help='字符画的长度。')
    parser.add_argument('-H', '--height', type=int, default=28,
                        help='字符画的高度。')
    parser.add_argument('-t', '--table', type=str, default='好　',
                        help='字符的列表。')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    text = image2charaterpainting(image_path=args.input, out_size=(args.width, args.height), char_table=args.table)
    save_txt(text, outpath=args.output)

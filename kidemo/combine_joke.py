# -*- coding: utf-8 -*-
# author: kuangdd
# date: 2020/9/19
"""
### 生成幽默笑话的markdown文本。
combine_joke

* 从幽默数据库导出幽默笑话，人工审核，如果选择则拟定标题，选择10则幽默笑话组成文档。
* 生成md文本的幽默笑话底稿。
"""
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(Path(__name__).stem)

import os


def load_jokes(fpath):
    """导入幽默笑话数据。"""
    if not os.path.exists(fpath):
        return []
    outs = []
    with open(fpath, encoding='utf8') as fout:
        for line in fout:
            idx, text, name = line.strip().split('\t')
            content = text.replace('    ', '\n\n').replace(' ', '\n')
            labels = name.split('|')
            out = dict(index=idx, text=content, label=labels)
            outs.append(out)
    return outs


def choose_jokes(jokes, history_jokes):
    """选择需要发布的幽默笑话。"""
    history_ids = {dt['index'] for dt in history_jokes}
    cnt = 0
    outs = []
    for dt in jokes:
        if cnt >= 10:
            title = input('请输入幽默笑话的主标题：\n')
            break
        flag = any([w == 'task2_train-5' for w in dt['label']]) and dt['index'] not in history_ids
        if flag:
            print('=' * 50)
            print(dt['text'])
            print('=' * 50)
            flag = input(f'请核对第【{cnt + 1}】个幽默笑话，选择【标题+回车】，舍弃【空格+回车】：\n')
            if flag.strip():
                out = dict(index=dt['index'], text=dt['text'], title=flag.strip())
                outs.append(out)
                cnt += 1
            else:
                out = dict(index=dt['index'], text=dt['text'], title='无')
                outs.append(out)
    return outs, title


def jokes_to_md(jokes, title):
    """整合选择的幽默笑话，生成markdown格式文本。"""
    outs = []
    outs.append(f'### {title}\n\n[片头图片](https://www.hippopx.com/zh)\n\n')
    for dt in jokes:
        idx, text, title = dt['index'], dt['text'], dt['title']
        if title != '无':
            out = f'#### {title}\n\n```\n{text}\n```\n\n\n'
            outs.append(out)
    outs.append('#### 啊啦嘻哈\n\n关注微信公众号“啊啦嘻哈”，回复“幽默笑话”，即可获得更多幽默笑话。\n\n')
    outs.append('[马克飞象](https://maxiang.io/)\n\n')
    joke_out = ''.join(outs)
    return joke_out


def save_md(joke, outpath):
    """保存生成的md格式的笑话文本。"""
    with open(outpath, 'wt', encoding='utf8') as fout:
        fout.write(joke)


def md_to_html(inpath, outpath):
    """把md格式的文本渲染为html。"""
    from md_to_html import Markdown2Html
    m2h = Markdown2Html('theme/whitelines.css')
    m2h.convert(inpath, outpath)


def save_history_jokes(jokes, outpath):
    """保存已经看过的幽默笑话。"""
    with open(outpath, 'at', encoding='utf8') as fout:
        for dt in jokes:
            idx, text, title = dt['index'], dt['text'], dt['title']
            text = text.replace('\n', '  ')
            fout.write(f'{idx}\t{text}\t{title}\n')


def main():
    """主流程。"""
    totalpath = r'joke/joke_v2.txt'
    historypath = r'joke/joke_history.txt'
    jokes = load_jokes(totalpath)
    jokes_history = load_jokes(historypath)
    jokes_choice, title = choose_jokes(jokes, jokes_history)
    joketext = jokes_to_md(jokes_choice, title)

    cnt = 1
    while True:
        mdpath = r'data/jokes/my_joke_{:03d}.md'.format(cnt)
        print(mdpath)
        if not os.path.exists(mdpath):
            break
        cnt += 1

    save_md(joketext, mdpath)
    save_history_jokes(jokes_choice, historypath)

    htmlpath = os.path.splitext(mdpath)[0] + '.html'
    md_to_html(mdpath, htmlpath)


if __name__ == "__main__":
    print(__file__)
    main()

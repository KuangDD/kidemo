# -*- coding: utf-8 -*-
# author: kuangdd
# date: 2020/9/10
"""
preprocess


cn_train.csv:
ID,Dialogue_id,Utterance_id,Speaker,Sentence,Label
0,0,0,卖油条小刘,我说,0
1,0,1,保姆小张,干啥子嘛？,0


en_train.csv:
ID,Dialogue_id,Utterance_id,Speaker,Sentence,Label
0,0,0,Chandler,also I was the point person on my companys transition from the KL-5 to GR-6 system.,0
1,0,1,The Interviewer,You mustve had your hands full.,0


humor_category_train.txt:
学校放假两天……请告知你们行李的重量。－－二男士。	3
一天……我们晚饭喝汤。”	3


humor_degree_train.txt:
一天……他们很干脆的离了婚成了至亲的朋友。	1
课堂上我举手问老师……心满意足地趴桌子上酣然大睡了	5


task1_train.csv:
id,joke,label
0,如果素食者只吃蔬菜，那么人道主义者呢？,1
1,妻子：亲爱的，请告诉我，我是你的最爱吗？ 丈夫：不，亲爱的！你是我的最最最爱。,1


task2_train.csv:
id,joke,label
0,阿华到市场买牛肉准备回家做料理……要带回家的啦！,1
1,小伙子向心爱的女友求婚！……那就和钻石绑在一起吧！”,3


yinyu_senti_train.txt:
思想的花开在路上。	2
他诚心当所有人面整服务员	6


yinyu_type_train.txt:
清真寺的气势盖过王宫，盖过这个城市的任何建筑，遍布城市的清真寺时时撞击游人的视觉，使人们想到伊斯坦布尔，脑海里浮现的就是清真寺。	1
爱情就像棉花糖，柔软而又甜蜜。	2


yishengxiaohua.txt:
女人是毒药	    比尔情场失意……老是想服毒自杀。”
戴错的戒指	    阿奎娜是一所大学的讲师……因为我嫁错人了。”


zhongguoxiaolindaquan.txt:
自讨没趣	某甲想拜见新到任的县官套套近乎……恐怕遇到大赦就会出来吧！”	——魏·邯郸淳《笑林》
有其父必有其子	齐国有一个富人……有这么愚蠢的父亲才生这么愚蠢的儿子啊！”	——旧题宋·苏轼《艾子杂说》


mingrenyoumo.txt:
智斗强盗	有一次，卓别林带着一大笔现款走在路上。……卓别林知道强盗的手枪里再也没有子弹了，便一脚把他绊倒，飞也似地跑了。
总统的滋味	有一次，林肯总统在白宫会见某国总统．……＂我感觉到天天像吃了火药，总想放炮！＂


dialog.txt:
ID	Dialogue_id	Utterance_id	Speaker	Sentence	Raw_id
00000000	000000	0000	经理	（男女均可）	1
00000001	000000	0001	小鲜肉	男、（可女人反串）	1


joke.txt:
汇总笑话数据

humor_category_train.txt
humor_degree_train.txt
task1_train.csv
task2_train.csv
yishengxiaohua.txt
zhongguoxiaolindaquan.txt
mingrenyoumo.txt

"""
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(Path(__name__).stem)

import re
import collections as clt
import phkit

_zh_re = re.compile(r'\w+')
_u200x_re = re.compile(r'[\u200b\u200c\u200d\u200e\u200f\ufeff]+')
_blank_re = re.compile(r'\s+')


def run_dialog():
    """
    ID,Dialogue_id,Utterance_id,Speaker,Sentence,Raw_id
    0,0,0,卖油条小刘,我说,0
    1,0,1,保姆小张,干啥子嘛？,0

    :return:
    """
    indir = Path('joke/dialog')
    outs = []
    cnt_id = 0
    for dia_id, fpath in enumerate(sorted(indir.glob('*.txt'), key=lambda x: int(x.stem))):
        with open(fpath, encoding='utf8') as fin:
            for utt_id, line in enumerate(fin):
                parts = line.split(':')
                spk = parts[0]
                sen = ':'.join(parts[1:]).strip()
                sen = sen.replace('\t', '')
                raw_id = fpath.stem
                outs.append([f'{cnt_id:08d}', f'{dia_id:06d}', f'{utt_id:04d}', spk, sen, raw_id])
                cnt_id += 1

    outpath = Path('joke/dialog_out.txt')
    with open(outpath, 'wt', encoding='utf8') as fout:
        fout.write('ID\tDialogue_id\tUtterance_id\tSpeaker\tSentence\tRaw_id\n')
        for line in outs:
            fout.write('\t'.join(line) + '\n')


def run_train_txt():
    """
    humor_category_train.txt:
    学校放假两天……请告知你们行李的重量。－－二男士。	3
    一天……我们晚饭喝汤。”	3

    task1_train.csv:
    id,joke,label
    0,如果素食者只吃蔬菜，那么人道主义者呢？,1
    1,妻子：亲爱的，请告诉我，我是你的最爱吗？ 丈夫：不，亲爱的！你是我的最最最爱。,1

    :return:
    """
    fnames = ('humor_category_train.txt humor_degree_train.txt task1_train.csv task2_train.csv '
              'yishengxiaohua.txt zhongguoxiaolindaquan.txt mingrenyoumo.txt').split()
    indir = Path('joke')
    outs = clt.defaultdict(list)
    cnt = 0
    for fname in fnames:
        fpath = indir.joinpath(fname)
        with open(fpath, encoding='utf8') as fin:
            for utt_id, line in enumerate(fin):
                if fpath.name.endswith('train.txt'):
                    parts = line.split('\t')
                    assert len(parts) == 2
                    sen = ''.join(parts[:-1]).strip()
                    lab = parts[-1].strip()
                    assert lab.isdigit()
                elif fpath.name.endswith('train.csv'):
                    parts = line.split(',')
                    sen = ','.join(parts[1:-1]).strip()
                    lab = parts[-1].strip()
                    try:
                        assert lab.isdigit()
                    except:
                        print(line)
                        print(fpath.name)
                elif fpath.name.endswith('.txt'):
                    parts = line.split('\t')
                    assert len(parts) in {2, 3}
                    sen = parts[1].strip()
                    lab = parts[0].strip()

                if lab != '0':
                    cnt += 1
                    outs[sen].append(fpath.stem + '-' + lab)
    print(len(outs))
    print(cnt)

    outpath = Path('joke/joke_out.txt')
    with open(outpath, 'wt', encoding='utf8') as fout:
        for num, (sen, labs) in enumerate(outs.items(), 1):
            sen = reformat_text(sen)
            fout.write(f'{num:08d}\t{sen}\t{"|".join(labs)}\n')


def reformat_text(text: str):
    """
    文本格式化。
    1.繁体转简体。
    2.全角转半角。
    3.去除零长度字符。
    4.各种空格字符都转为空格。
    5.无文字的标点拼接到前一句话结尾。
    6.大段4个空格，小段1个空格。
    :param text:
    :return:
    """
    parts = text.split('    ')
    text_out = []
    for num, line in enumerate(parts):
        out = phkit.fan2jian(line)
        out = phkit.quan2ban(out)
        out = _u200x_re.sub('', out)
        out = _blank_re.sub(' ', out)
        if ' ' in out:
            tmp_outs = []
            tmp = out.split()
            flag = False
            for i, w in enumerate(tmp):
                if not _zh_re.search(w):
                    if i >= 1 or flag:
                        tmp_outs[-1] = tmp_outs[-1] + w
                    else:
                        tmp_outs.append(w)

                    if w == '-':
                        flag = True
                    else:
                        flag = False
                        # print(tmp[max(0, i - 1): i + 2])
                else:
                    tmp_outs.append(w)
            out = ' '.join(tmp_outs)

            # for w in tmp_outs:
            #     print(w)
            # print('=' * 50)
        text_out.append(out)
    text_out = '    '.join(text_out)
    return text_out


if __name__ == "__main__":
    print(__file__)
    # run_dialog()
    run_train_txt()

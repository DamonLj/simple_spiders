# -*- coding:utf-8 -*-

import os

filepath = os.path.dirname(__file__)
filepath1 = os.path.join(os.path.dirname(filepath), 'gintama.txt')
filepath2 = os.path.join(filepath, 'gintamatitle.txt')
with open(filepath1, 'r', encoding='utf8') as f:
    title_d = [eval(x) for x in f.readlines()]
gintamatitle = [x['gintamatitle'] for x in title_d]
with open(filepath2, 'w', encoding='utf8') as f:
    f.writelines(str(x) + '\n' for x in gintamatitle)

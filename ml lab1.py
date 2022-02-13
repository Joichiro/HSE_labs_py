from collections import namedtuple
from datetime import datetime
from math import erfc, fabs
#import pickle
from random import random, choice
import re

import numpy as np
import pandas as pd
from requests import get
from sklearn import preprocessing

pd.set_option('display.width', 4096)
pd.set_option('display.max_colwidth', 1024)
pd.set_option('display.max_rows', 1024)
pd.set_option('display.max_columns', 64)
pd.set_option('display.precision', 4)

Data = namedtuple('Data', 'subject pages answers last_date last_author rnd_number')

r = get('https://forum.ixbt.com/?id=82')
#r = pickle.Unpickler(open('ixbt82.dump', 'rb')).load()
# f_tr(82,675,'n1',0,53,'"Умный дом" своими руками.',1302,135796,'','Delfin',1268215740,'4shirsky',1644604860,'')
# f_tr(82,1546,'n1',0,1,'Работа с DVR на ПК через ...',10,15600,'','z12345678',1421924220,'rb8',1642758240,'')
# f_tr( #,   #,  #, #,pages, subj,                answers,    #,'',         #,      #, last_author, last_date, '')
xs = re.findall(r'f_tr\(\d+,\d+,\S+?,\d+,(\d+),\'(.+?)\',(\d+),\d+,\'\',\'.+?\',\d+,'
                r'\'(<span .+?</span>)?(.+?)\',(\d+),\'\'\)', r.text)
zs = pd.DataFrame([Data(x[1], int(x[0]), int(x[2]), datetime.fromtimestamp(int(x[5])),
                        x[4], random() * 2.0 - 1.0) for x in xs])

print('1. Данные с веб-страницы')
print(zs)
print('\n\n')

word1 = 'дом дома дому домом доме домов домам домами домах'
word2 = 'квартира квартиры квартире квартиру квартирой квартирою квартир квартирам квартирами квартирах'
rgx = re.compile(r'\b(' + (word1 + ' ' + word2).replace(' ', '|') + r')\b', re.IGNORECASE)
#zs2 = zs[(zs['subject'].apply(lambda x: bool(rgx.search(x)))) & (zs['answers'] >= 50)]
zs2 = zs[(zs.subject.apply(lambda x: bool(rgx.search(x)))) & (zs.answers >= 50)]

print('2. Данные с веб-страницы с темами со словом "дом" или "квартира" с числом ответов не менее 50')
print(zs2)
print('\n\n')

scaler = preprocessing.StandardScaler()
zs3 = zs.copy()
zs3.loc[:, ['pages', 'answers', 'rnd_number']] = scaler.fit_transform(zs[['pages', 'answers', 'rnd_number']])

print('3. Нормализованные данные')
print(zs3)
print('\n\n')

rnd_col = choice(['pages', 'answers', 'rnd_number'])
rnd_row = choice(zs3.index)
old_value = zs3.loc[rnd_row, rnd_col]
zs3.loc[rnd_row, rnd_col] = np.nan
zs4 = zs3[zs3[rnd_col].notna()]
zs5 = zs3[zs3[rnd_col].isnull()]
correls = {}
for col in ['pages', 'answers', 'rnd_number']:
    if col != rnd_col:
        correls[col] = np.corrcoef(zs4[col], zs4[rnd_col])[0][1]
new_value = (zs4.loc[:, rnd_col].mean()
             + ((1.0 / sum([fabs(x) for x in correls.values()]))
                 * sum([x * (zs5.iloc[0][col] - zs4[col].mean()) for col, x in correls.items()])))
zs3.loc[rnd_row, rnd_col] = new_value

print('4. Удаление и восстановление')
print(f'row={rnd_row}  column={rnd_col}  old_value={old_value:.4}  new_value={new_value:.4}')
print('\n\n')

while True:
    mean = zs3.pages.mean()
    stdev = zs3.pages.std()
    if np.isclose(stdev, 0.0):
        break
    if zs3.pages.count() == 0:
        break
    lim = 1.0 / (2.0 * zs3.pages.count())
    idx = zs3.pages.apply(lambda x: True if erfc(fabs(x - mean) / stdev) < lim else None).first_valid_index()
    if idx is None:
        break
    #erfc_ = erfc(fabs(zs3.pages[idx] - mean) / stdev)
    #print(f'{mean=:.3f}  {stdev=:.3f} {erfc_=:.3f}  {lim=:.3f}  {idx=}  {zs3.pages[idx]=:.3f}')
    zs3 = zs3.drop(index=idx)

print('5. Нормализованные данные с удаленными выбросами в столбце с количеством страниц')
print(zs3)
print('\n\n')


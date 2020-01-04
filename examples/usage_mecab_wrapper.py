# -*- coding: utf-8 -*-
from janome.wrappers.mecab import Tokenizer
import sys
from io import open

print(u'Tokenize (system dictionary)')
t = Tokenizer()
for token in t.tokenize(u'すもももももももものうち'):
  print(token)

print('')
print(u'Tokenize (wakati mode)')
for token in t.tokenize(u'すもももももももものうち', wakati = True):
  print(token)

print(u'Tokenize (stream mode)')
t = Tokenizer()
with open('text_lemon.txt', encoding='utf-8') as f:
    text = f.read()
    for token in t.tokenize(text):
        print(token)

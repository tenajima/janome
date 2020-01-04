import cProfile
from janome.tokenizer import Tokenizer
from janome.wrappers.mecab import Tokenizer as MeCabTokenizer

t = Tokenizer()
#t = MeCabTokenizer()

with open('text_lemon.txt', encoding='utf-8') as f:
    s = f.read()

cProfile.run('for i in range(100): t.tokenize(s)')
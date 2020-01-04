# -*- coding: utf-8 -*-

# Copyright 2015 moco_beta
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, sys
from io import open

# TODO: better way to find package...
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from janome.wrappers.mecab import Tokenizer as MeCabTokenizer, UnsupportedPlatformException
from janome.lattice import NodeType

import unittest

class TestMeCabTokenizer(unittest.TestCase):

    def test_mecab_tokenize(self):
        text = u'すもももももももものうち'
        tokens = MeCabTokenizer().tokenize(text)
        self.assertEqual(7, len(tokens))
        self._check_token(tokens[0], u'すもも', u'名詞,一般,*,*,*,*,すもも,スモモ,スモモ')
        self._check_token(tokens[1], u'も', u'助詞,係助詞,*,*,*,*,も,モ,モ')
        self._check_token(tokens[2], u'もも', u'名詞,一般,*,*,*,*,もも,モモ,モモ')
        self._check_token(tokens[3], u'も', u'助詞,係助詞,*,*,*,*,も,モ,モ')
        self._check_token(tokens[4], u'もも', u'名詞,一般,*,*,*,*,もも,モモ,モモ')
        self._check_token(tokens[5], u'の', u'助詞,連体化,*,*,*,*,の,ノ,ノ')
        self._check_token(tokens[6], u'うち', u'名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ')
        
    def test_mecab_tokenize2(self):
        text = u'𠮷野屋'
        tokens = MeCabTokenizer().tokenize(text)
        self.assertEqual(3, len(tokens))
        self._check_token(tokens[0], u'𠮷', u'記号,一般,*,*,*,*,*,*,*')
        self._check_token(tokens[1], u'野', u'名詞,一般,*,*,*,*,野,ノ,ノ')
        self._check_token(tokens[2], u'屋', u'名詞,接尾,一般,*,*,*,屋,ヤ,ヤ')

        text = u'한국어'
        tokens = MeCabTokenizer().tokenize(text)
        self.assertEqual(1, len(tokens))
        self._check_token(tokens[0], u'한국어', u'記号,一般,*,*,*,*,*,*,*')

    def test_mecab_tokenize_unknown(self):
        text = u'2009年10月16日'
        tokens = MeCabTokenizer().tokenize(text)
        self.assertEqual(6, len(tokens))
        self._check_token(tokens[0], u'2009', u'名詞,数,*,*,*,*,*,*,*')
        self._check_token(tokens[1], u'年', u'名詞,接尾,助数詞,*,*,*,年,ネン,ネン')
        self._check_token(tokens[2], u'10', u'名詞,数,*,*,*,*,*,*,*')
        self._check_token(tokens[3], u'月', u'名詞,一般,*,*,*,*,月,ツキ,ツキ')
        self._check_token(tokens[4], u'16', u'名詞,数,*,*,*,*,*,*,*')
        self._check_token(tokens[5], u'日', u'名詞,接尾,助数詞,*,*,*,日,ニチ,ニチ')

        text = u'マルチメディア放送（VHF-HIGH帯）「モバキャス」'
        tokens = MeCabTokenizer().tokenize(text)
        self.assertEqual(11, len(tokens))
        self._check_token(tokens[0], u'マルチメディア', u'名詞,一般,*,*,*,*,マルチメディア,マルチメディア,マルチメディア')
        self._check_token(tokens[1], u'放送', u'名詞,サ変接続,*,*,*,*,放送,ホウソウ,ホーソー')
        self._check_token(tokens[2], u'（', u'記号,括弧開,*,*,*,*,（,（,（')
        self._check_token(tokens[3], u'VHF', u'名詞,固有名詞,組織,*,*,*,*,*,*')
        self._check_token(tokens[4], u'-', u'名詞,サ変接続,*,*,*,*,*,*,*')
        self._check_token(tokens[5], u'HIGH', u'名詞,一般,*,*,*,*,*,*,*')
        self._check_token(tokens[6], u'帯', u'名詞,接尾,一般,*,*,*,帯,タイ,タイ')
        self._check_token(tokens[7], u'）', u'記号,括弧閉,*,*,*,*,）,）,）')
        self._check_token(tokens[8], u'「', u'記号,括弧開,*,*,*,*,「,「,「')
        self._check_token(tokens[9], u'モバキャス', u'名詞,固有名詞,一般,*,*,*,*,*,*')
        self._check_token(tokens[10], u'」', u'記号,括弧閉,*,*,*,*,」,」,」')

    def test_mecab_tokenize_large_text(self):
        with open('tests/text_lemon.txt', encoding='utf-8') as f:
            text = f.read()
            tokens = MeCabTokenizer().tokenize(text)

    def test_mecab_tokenize_large_text2(self):
        with open('tests/text_large.txt', encoding='utf-8') as f:
            text = f.read()
            tokens = MeCabTokenizer().tokenize(text)

    def test_mecab_tokenize_large_text3(self):
        with open('tests/text_large_nonjp.txt', encoding='utf-8') as f:
            text = f.read()
            tokens = MeCabTokenizer().tokenize(text)

    def test_mecab_tokenize_large_text_stream(self):
        with open('tests/text_lemon.txt', encoding='utf-8') as f:
            text = f.read()
            tokens = list(MeCabTokenizer().tokenize(text, stream = True))

    def test_mecab_tokenize_large_text_stream2(self):
        with open('tests/text_large.txt', encoding='utf-8') as f:
            text = f.read()
            tokens = list(MeCabTokenizer().tokenize(text, stream = True))

    def test_mecab_tokenize_large_text_stream3(self):
        with open('tests/text_large_nonjp.txt', encoding='utf-8') as f:
            text = f.read()
            tokens = list(MeCabTokenizer().tokenize(text, stream = True))

    def test_mecab_tokenize_wakati(self):
        text = u'すもももももももものうち'
        
        tokens = MeCabTokenizer(wakati = True).tokenize(text)
        self.assertEqual(7, len(tokens))
        self.assertEqual(tokens[0], u'すもも')
        self.assertEqual(tokens[1], u'も')
        self.assertEqual(tokens[2], u'もも')
        self.assertEqual(tokens[3], u'も')
        self.assertEqual(tokens[4], u'もも')
        self.assertEqual(tokens[5], u'の')
        self.assertEqual(tokens[6], u'うち')

        tokens = MeCabTokenizer().tokenize(text, wakati = True)
        self.assertEqual(7, len(tokens))
        self.assertEqual(tokens[0], u'すもも')
        self.assertEqual(tokens[1], u'も')
        self.assertEqual(tokens[2], u'もも')
        self.assertEqual(tokens[3], u'も')
        self.assertEqual(tokens[4], u'もも')
        self.assertEqual(tokens[5], u'の')
        self.assertEqual(tokens[6], u'うち')

    def test_mecab_tokenize_wakati_mode_only(self):
        text = u'すもももももももものうち'
        tokens = MeCabTokenizer(wakati = True).tokenize(text, wakati = False)
        # 'wakati = True' parameter is ignored.
        self.assertEqual(7, len(tokens))
        self.assertEqual(tokens[0], u'すもも')
        self.assertEqual(tokens[1], u'も')
        self.assertEqual(tokens[2], u'もも')
        self.assertEqual(tokens[3], u'も')
        self.assertEqual(tokens[4], u'もも')
        self.assertEqual(tokens[5], u'の')
        self.assertEqual(tokens[6], u'うち')

    def _check_token(self, token, surface, detail):
        self.assertEqual(surface, token.surface)
        self.assertEqual(detail, ','.join([token.part_of_speech,token.infl_type,token.infl_form,token.base_form,token.reading,token.phonetic]))
        self.assertEqual(surface + '\t' + detail, str(token))

if __name__ == '__main__':
    unittest.main()

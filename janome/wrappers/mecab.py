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

import ctypes as C
import platform

from ..lattice import NodeType

DEFAULT_LIBMECAB_NAME_LINUX = 'libmecab.so'
SUPPORTED_PLATFORM = [('Linux', DEFAULT_LIBMECAB_NAME_LINUX)]

# mecab node stat
MECAB_NOR_NODE = 0
MECAB_UNK_NODE = 1
MECAB_BOS_NODE = 2
MECAB_EOS_NODE = 3
MECAB_EON_NODE = 4

class UnsupportedPlatformException(Exception):
    def __init__(self, runtime_pf):
        self.message = "Supported platforms are %s; got %s" % (', '.join(t[0] for t in SUPPORTED_PLATFORM), runtime_pf)

class MeCabTagger(C.Structure):
    pass

#class MeCabNode(C.Structure):
#    _fields_ = [
#        ('prev', C.c_void_p), ('next', C.c_void_p), ('enext', C.c_void_p), ('bnext', C.c_void_p), ('rpath', C.c_void_p), ('lpath', C.c_void_p),
#        ('surface', C.c_char_p), ('feature', C.c_char_p), ('id', C.c_uint), ('length', C.c_ushort), ('rlength', C.c_ushort),
#        ('rcAttr', C.c_ushort), ('lcAttr', C.c_ushort), ('posid', C.c_ushort), ('char_type', C.c_ubyte), ('stat', C.c_ubyte), ('isbest', C.c_ubyte),
#        ('alpha', C.c_float), ('beta', C.c_float), ('prob', C.c_float), ('wcost', C.c_short), ('cost', C.c_long)
#    ]

class Token:

    __slots__ = ['mecab_token', 'mecab_char_enc', '__surface', '__features']

    def __init__(self, mecab_token, mecab_char_enc):
        self.mecab_token = mecab_token
        self.mecab_char_enc = mecab_char_enc

    def __str__(self):
        return '%s\t%s,%s,%s,%s,%s,%s' % \
           (self.surface, self.part_of_speech, self.infl_type, self.infl_form, self.base_form, self.reading, self.phonetic)

    @property
    def surface(self):
        if not hasattr(self, '__surface'):
            self.__surface = self.mecab_token.decode(self.mecab_char_enc).split('\t')[0]
        return self.__surface
        
    @property
    def part_of_speech(self):
        """part of speech (品詞)"""
        return ','.join(self.features[0:4])

    @property
    def infl_type(self):
        """terminal form (活用型)"""
        return self.features[4]

    @property
    def infl_form(self):
        """stem form (活用形)"""
        return self.features[5]

    @property
    def base_form(self):
        """base form (基本形)"""
        return self.features[6]
    
    @property
    def reading(self):
        """"reading (読み)"""
        return self.features[7] if len(self.features) > 7 else '*'

    @property
    def phonetic(self):
        """pronounce (発音)"""
        return self.features[8] if len(self.features) > 8 else '*'

    @property
    def node_type(self):
        return self.get_node_type(self.mecab_node)

    @property
    def features(self):
        if not hasattr(self, '__features'):
            self.__features = self.mecab_token.decode(self.mecab_char_enc).split('\t')[1].split(',')
        return self.__features


class Tokenizer:
    def __init__(self, libmecab_name=None, mecab_char_enc='utf8', wakati=False):
        self.wakati = wakati
        self.mecab_char_enc = mecab_char_enc
        self.__load_libmecab(libmecab_name)

    def __load_libmecab(self, libmecab_name):
        runtime_pf = platform.platform()
        success = False
        for (pf, def_libmecab) in SUPPORTED_PLATFORM:
            if runtime_pf.find(pf) >= 0:
                self.libmecab = C.CDLL(libmecab_name if libmecab_name else def_libmecab)
                self.libmecab.mecab_new2.argtypes = [C.c_char_p]
                self.libmecab.mecab_new2.restype = C.POINTER(MeCabTagger)
                #self.libmecab.mecab_sparse_tonode.argtypes = [C.c_void_p, C.c_char_p]
                #self.libmecab.mecab_sparse_tonode.restype = C.POINTER(MeCabNode)
                self.libmecab.mecab_sparse_tostr.argtypes = [C.c_void_p, C.c_char_p]
                self.libmecab.mecab_sparse_tostr.restype = C.c_char_p
                success = True
                break
        if not success:
            raise UnsupportedPlatformException(runtime_pf)
        
    def tokenize(self, text, stream=False, wakati=False):
        if self.wakati:
            wakati = True
        tagger = self.libmecab.mecab_new2(b'mecab')
        try:
            if stream:
                return self.__tokenize_stream(text, tagger, wakati)
            else:
                return list(self.__tokenize_stream(text, tagger, wakati))
        finally:
            self.libmecab.mecab_destroy(tagger)

    def __tokenize_stream(self, text, tagger, wakati):
        lines = text.encode(self.mecab_char_enc).splitlines()
        for line in lines:
            for token in self.__tokenize_line(line, tagger, wakati):
                yield token

    def __tokenize_line(self, line, tagger, wakati):
        mecab_res = self.libmecab.mecab_sparse_tostr(tagger, line)
        res = []
        for token in mecab_res.splitlines():
            if token == b'EOS':
                continue
            if wakati:
                surface = token.decode(self.mecab_char_enc).split('\t')[0]
                res.append(surface)
            else:
                res.append(Token(token, self.mecab_char_enc))
        return res



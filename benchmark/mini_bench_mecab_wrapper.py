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

setup = """
from janome.wrappers.mecab import Tokenizer
t = Tokenizer()
with open('text_lemon.txt', encoding='utf-8') as f:
    s = f.read()
"""

stmt = """
(token.surface for token in t.tokenize(s))
"""

if __name__ == '__main__':
    import timeit, sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10

    print("** initialize Tokenizer object **")
    print(timeit.timeit(stmt='Tokenizer()', setup='from janome.wrappers.mecab import Tokenizer', number=1))

    print("** execute tokenize() %d times **" % n)
    res = timeit.repeat(stmt=stmt, setup=setup, repeat=1, number=n)
    for i, x in enumerate(res):
        print("repeat %d: %f" % (i, x / n))

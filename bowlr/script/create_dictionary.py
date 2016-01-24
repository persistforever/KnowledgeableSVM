# -*- encoding = gb18030 -*-

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../..'))

from bowlr.run import Corpus
# package importing end


# run this script

article_market_path = sys.argv[1]
dictionary_path = sys.argv[2]
dict_set = sys.argv[3]
corpus = Corpus()
corpus.run_create_dictionary(article_market_path, dictionary_path, dict_set)
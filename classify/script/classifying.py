﻿# -*- encoding = gb18030 -*-

# package importing start
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../..'))

from classify.run import Corpus
# package importing end


# run this script

train_path = sys.argv[1]
test_path = sys.argv[2]
train_set = sys.argv[3]
test_set = sys.argv[4]
corpus = Corpus()
corpus.run_classify(train_path, test_path, train_set, test_set)
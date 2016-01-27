type=car

article_market_path=E:/data/knowledge/bowlr/$type/article_trainset_market
dictionary_path=E:/data/knowledge/bowlr/all/dictionary
dict_set=$1

python E://github/WechatKnowledge/KnowledgeableSVM/KnowledgeableSVM/bowlr/script/create_dictionary.py \
				$article_market_path $dictionary_path $dict_set
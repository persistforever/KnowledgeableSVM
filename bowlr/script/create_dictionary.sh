type=car

article_market_path=E:/file/knowledge/classify/$type/article_trainset_market
dictionary_path=E:/file/knowledge/classify/all/dictionary
dict_set=$1

python E://github/WechatKnowledge/KnowledgeableSVM/KnowledgeableSVM/bowlr/script/create_dictionary.py \
				$article_market_path $dictionary_path $dict_set
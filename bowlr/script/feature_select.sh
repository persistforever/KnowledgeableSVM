type=$1

article_market_path=E:/file/knowledge/classify/$type/article_trainset_market
dictionary_path=E:/file/knowledge/classify/all/dictionary
feature_market_path=E:/file/knowledge/classify/$type/trainset_feature_market

python E://github/WechatKnowledge/KnowledgeableSVM/KnowledgeableSVM/bowlr/script/feature_select.py \
				$article_market_path $dictionary_path $feature_market_path

				
article_market_path=E:/file/knowledge/classify/$type/article_testset_market
dictionary_path=E:/file/knowledge/classify/all/dictionary
feature_market_path=E:/file/knowledge/classify/$type/testset_feature_market

python E://github/WechatKnowledge/KnowledgeableSVM/KnowledgeableSVM/bowlr/script/feature_select.py \
				$article_market_path $dictionary_path $feature_market_path
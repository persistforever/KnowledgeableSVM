type=$1

article_market_path=E:/data/knowledge/bowlr/$type/article_trainset_market
dictionary_path=E:/data/knowledge/bowlr/all/dictionary
feature_market_path=E:/data/knowledge/bowlr/$type/trainset_feature_market

python E://github/WechatKnowledge/KnowledgeableSVM/KnowledgeableSVM/bowlr/script/feature_select.py \
				$article_market_path $dictionary_path $feature_market_path

				
article_market_path=E:/data/knowledge/bowlr/$type/article_testset_market
dictionary_path=E:/data/knowledge/bowlr/all/dictionary
feature_market_path=E:/data/knowledge/bowlr/$type/testset_feature_market

python E://github/WechatKnowledge/KnowledgeableSVM/KnowledgeableSVM/bowlr/script/feature_select.py \
				$article_market_path $dictionary_path $feature_market_path
type=$1

articles_path=E:/data/knowledge/bowlr/$type/article_trainset
article_market_path=E:/data/knowledge/bowlr/$type/article_trainset_market

python E://github/WechatKnowledge/KnowledgeableSVM/KnowledgeableSVM/bowlr/script/convert_article.py \
				$articles_path $article_market_path

				
articles_path=E:/data/knowledge/bowlr/$type/article_testset
article_market_path=E:/data/knowledge/bowlr/$type/article_testset_market

python E://github/WechatKnowledge/KnowledgeableSVM/KnowledgeableSVM/bowlr/script/convert_article.py \
				$articles_path $article_market_path
train_type=car
test_type=car
train_set=$1
test_set=$2


train_path=E:/data/knowledge/classify/$train_type/trainset_feature_market
test_path=E:/data/knowledge/classify/$test_type/testset_feature_market

python E://github/WechatKnowledge/KnowledgeableSVM/KnowledgeableSVM/classify/script/classifying.py \
				$train_path $test_path $train_set $test_set
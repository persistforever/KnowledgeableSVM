# -*- encoding = gb18030 -*-
"""
This python file is noly used to Debug.
Can call different function to do different tasks.
If function func_name debug finished, please complete the wechat/main/func_name.py.
"""

# package importing start
# package importing end


    
def tag() :
    from tag.run import Corpus
    from file.path_manager import PathManager
    sentences_path = PathManager.CORPUS_ARTICLE
    tag_tree_path = PathManager.TAG_TAGTREE
    tags_path = PathManager.TAG_ARTICLETAG
    tags_market_path = PathManager.TAG_ARTICLETAG
    sentences_market_path = PathManager.TAG_SENTENCES
    untag_sentence_path = PathManager.TAG_UNTAGSENTENCE
    corpus = Corpus()
    corpus.run(sentences_path, tag_tree_path, sentences_market_path, tags_path, \
        tags_market_path, untag_sentence_path)
    print 'finish'
    
def pretreate() :
    from pretreate.run import Corpus
    from file.path_manager import PathManager
    articles_path = PathManager.CORPUS_ARTICLE
    participle_title_path = PathManager.CORPUS_SPLIT
    treated_article_path = PathManager.CORPUS_FEATURE
    corpus = Corpus()
    corpus.run(articles_path, participle_title_path, treated_article_path)
    
def classify() :
    from classify.run import Corpus
    from file.path_manager import PathManager
    articles_path='E:/data/knowledge/classify/car/article_trainset'
    article_market_path='E:/data/knowledge/classify/car/article_trainset_market'
    feature_path='E:/data/knowledge/classify/car/trainset_feature'
    feature_market_path='E:/data/knowledge/classify/car/trainset_feature_market'
    pos_path='E:/data/knowledge/tools/postag'
    punc_path='E:/data/knowledge/tools/punctuation'
    klword_path='E:/data/knowledge/tools/knowledgeable_word'
    train_path='E:/data/knowledge/classify/car/trainset_feature_market'
    test_path='E:/data/knowledge/classify/car/testset_feature_market'
    corpus = Corpus()
    corpus.run(articles_path, article_market_path, \
        pos_path, punc_path, klword_path, feature_path, feature_market_path, \
        train_path, test_path)
    
def embedding() :
    from embedding.run import Corpus
    from file.path_manager import PathManager
    articles_path = PathManager.CORPUS_ARTICLE
    participle_title_path = PathManager.CORPUS_SPLIT
    sentences_path = PathManager.CORPUS_KEYWORD
    word_embedding_path =PathManager.CORPUS_SIMPLYARTICLE
    corpus = Corpus()
    corpus.run(articles_path, participle_title_path, sentences_path, sentences_path, \
        word_embedding_path, word_embedding_path)
    
def bowlr() :
    from bowlr.run import Corpus
    from file.path_manager import PathManager
    articles_path='E:/data/knowledge/bowlr/car/article_trainset'
    article_market_path='E:/data/knowledge/bowlr/car/article_trainset_market'
    dictionary_path='E:/data/knowledge/bowlr/all/dictionary'
    feature_path='E:/data/knowledge/bowlr/car/trainset_feature'
    feature_market_path='E:/data/knowledge/bowlr/car/trainset_feature_market'
    train_path='E:/data/knowledge/bowlr/car/trainset_feature_market'
    test_path='E:/data/knowledge/bowlr/car/testset_feature_market'
    corpus = Corpus()
    corpus.run(articles_path, article_market_path, dictionary_path, feature_path, \
               feature_market_path, train_path, test_path)


if __name__ == '__main__' :
    # tag()
    # pretreate()
    classify()
    # embedding()
    # bowlr()
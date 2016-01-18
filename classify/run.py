﻿# -*- encoding = gb18030 -*-

# package importing start
import sys
import numpy as np

# import gensim

from basic.word import Word
from file.file_operator import TextFileOperator
from basic.market import PickleMarket, JsonMarket
import classify.selector as selector
from classify.classifier import SvmClassifier
# package importing end


class Corpus :

    def __init__(self) :
        pass

    def run(self, article_path, article_market_path, \
            pos_path, punc_path, klword_path, feature_path, feature_market_path, \
            train_path, test_path) :
        """ function for script to drive. """
        # self.run_convert_article(article_path, article_market_path)
        # self.run_feature_select(article_market_path, pos_path, punc_path, klword_path, \
        #                        feature_path, feature_market_path)
        self.run_classify(train_path, test_path)

    def run_convert_article(self,  article_path, article_market_path) :
        articles = self.read_article(article_path)
        # articles = self.read_participle(articles, participle_path)
        loader = PickleMarket()
        loader.dump_market(articles, article_market_path)
        print 'finish.'

    def run_feature_select(self, article_market_path, pos_path, punc_path, klword_path, \
        feature_path, feature_market_path) :
        loader = PickleMarket()
        pos_selector = selector.PosExtractor(pos_path, w=5, combined=True)
        token_selector = selector.TokenExtractor(punc_path)
        word_selector = selector.WordExtractor(klword_path, weight=1)
        articles = loader.load_market(article_market_path)
        length = len(articles) - 1
        for idx, article in enumerate(articles) :
            article['features'] = list()
            article['features'].extend(pos_selector.extract_feature(article['participle_content']))
            article['features'].extend(token_selector.extract_feature(article['title'], article['content'], \
                                                                        article['participle_title'], \
                                                                        article['participle_content']))
            article['features'].extend(word_selector.extract_feature(article['participle_title'], \
                                                                        article['participle_content']))
            print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        featuresets = [[article['id']] + article['features'] + [article['label']] for article in articles]
        file_operator = TextFileOperator()
        file_operator.writing(featuresets, feature_path)
        loader.dump_market(featuresets, feature_market_path)
        print 'finish'

    def run_classify(self, train_path, test_path) :
        loader = PickleMarket()
        # read train
        articles = list()
        for type in [u'car', u'finance', u'web'] :
            path = train_path.replace(u'all', type)
            articles.extend(loader.load_market(path))
        train_dataset = np.array([np.array(article[1:-1]) for article in articles])
        print train_dataset.shape
        train_label = np.array([np.array(int(article[-1])) for article in articles])
        # read test
        articles = list()
        for type in [u'car', u'finance', u'web'] :
            path = test_path.replace(u'all', type)
            articles.extend(loader.load_market(path))
        test_dataset = np.array([np.array(article[1:-1]) for article in articles])
        print test_dataset.shape
        test_label = np.array([np.array(int(article[-1])) for article in articles])
        # train cls
        classifier = SvmClassifier()
        train_dataset = classifier.normalize(train_dataset, method='mapminmax')
        test_dataset = classifier.normalize(test_dataset, method='mapminmax')
        classifier.training(train_dataset, train_label, cset=range(10, 100, 10), kernel='linear')
        # test cls
        test_prob = classifier.testing(test_dataset, type='prob')
        test_class = classifier.testing(test_dataset, type='label')
        print 'performance is', classifier.evaluation(test_label, test_prob, test_class)
        print 'finish'

    def run_optimize_params(self, train_article_market_path, test_article_market_path, \
        pos_path, punc_path, klword_path, logger_path) :
        loader = PickleMarket()
        logger = list()
        logger.append(['w', 'combined', 'weight', 'kernel', 'c', 'norm', 'car_car', \
            'car_finance', 'car_web', 'finance_car', 'finance_finance', 'finance_web', \
            'web_car', 'web_fiannce', 'web_web', 'merge_car', 'merge_finance', 'merge_web'])
        domains = [u'car', u'finance', u'web']
        wset = [5, 10, 15, 20]
        combinedset = [True, False]
        weightset = [1, 2, 5]
        kernelset = ['linear', 'poly', 'rbf']
        cset = [range(10, 100, 10), range(100, 1000, 100)]
        normset = ['mapminmax', 'zscore']
        token_selector = selector.TokenExtractor(punc_path)
        for w in wset :
            for combined in combinedset :
                pos_selector = selector.PosExtractor(pos_path, w=w, combined=combined)
                for weight in weightset :
                    word_selector = selector.WordExtractor(klword_path, weight=weight)
                    train_featuresets, test_featuresets = list(), list()
                    for step in range(len(domains)) :
                        train_featuresets.append(list())
                        test_featuresets.append(list())
                    for index, domain in enumerate(domains) :
                        train_articles = loader.load_market(train_article_market_path.replace(u'all', domain))
                        test_articles = loader.load_market(test_article_market_path.replace(u'all', domain))
                        # train
                        length = len(train_articles) - 1
                        for idx, article in enumerate(train_articles) :
                            article['features'] = list()
                            article['features'].extend(pos_selector.extract_feature(article['participle_content']))
                            article['features'].extend(token_selector.extract_feature(article['title'], article['content'], \
                                                                                        article['participle_title'], \
                                                                                        article['participle_content']))
                            article['features'].extend(word_selector.extract_feature(article['participle_title'], \
                                                                                        article['participle_content']))
                            print 'finish rate is %.2f%%\r' % (100.0*idx/length),
                        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
                        train_featuresets[index] = [[article['id']] + article['features'] + [article['label']] for article in train_articles]
                        # test
                        length = len(test_articles) - 1
                        for idx, article in enumerate(test_articles) :
                            article['features'] = list()
                            article['features'].extend(pos_selector.extract_feature(article['participle_content']))
                            article['features'].extend(token_selector.extract_feature(article['title'], article['content'], \
                                                                                        article['participle_title'], \
                                                                                        article['participle_content']))
                            article['features'].extend(word_selector.extract_feature(article['participle_title'], \
                                                                                        article['participle_content']))
                            print 'finish rate is %.2f%%\r' % (100.0*idx/length),
                        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
                        test_featuresets[index] = [[article['id']] + article['features'] + [article['label']] for article in test_articles]
                    for kernel in kernelset :
                        for c in cset :
                            for norm in normset :
                                evl = list()
                                for train_idx in range(0, len(domains)) :
                                    for test_idx in range(0, len(domains)) :
                                        train_dataset = np.array([np.array(article[1:-1]) for article in train_featuresets[train_idx]])
                                        train_label = np.array([np.array(int(article[-1])) for article in train_featuresets[train_idx]])
                                        test_dataset = np.array([np.array(article[1:-1]) for article in test_featuresets[test_idx]])
                                        test_label = np.array([np.array(int(article[-1])) for article in test_featuresets[test_idx]])
                                        classifier = SvmClassifier()
                                        train_dataset = classifier.normalize(train_dataset, method=norm)
                                        test_dataset = classifier.normalize(test_dataset, method=norm)
                                        classifier.training(train_dataset, train_label, cset=c, kernel=kernel)
                                        test_prob = classifier.testing(test_dataset, type='prob')
                                        test_class = classifier.testing(test_dataset, type='label')
                                        evl.append(classifier.evaluation(test_label, test_prob, test_class)[1])
                                print 'single finished ...'
                                # merge
                                articles = list()
                                for train_idx in range(0, len(domains)) :
                                    articles.extend(train_featuresets[train_idx])
                                train_dataset = np.array([np.array(article[1:-1]) for article in articles])
                                train_label = np.array([np.array(int(article[-1])) for article in articles])
                                for test_idx in range(0, len(domains)) :
                                    test_dataset = np.array([np.array(article[1:-1]) for article in test_featuresets[test_idx]])
                                    test_label = np.array([np.array(int(article[-1])) for article in test_featuresets[test_idx]])
                                    classifier = SvmClassifier()
                                    train_dataset = classifier.normalize(train_dataset, method=norm)
                                    test_dataset = classifier.normalize(test_dataset, method=norm)
                                    classifier.training(train_dataset, train_label, cset=c, kernel=kernel)
                                    test_prob = classifier.testing(test_dataset, type='prob')
                                    test_class = classifier.testing(test_dataset, type='label')
                                    evl.append(classifier.evaluation(test_label, test_prob, test_class)[1])
                                print 'merge finished ...'
                                print 'performance is', 1.0*sum(evl)/len(evl)
                                log = [w, combined, weight, kernel, c[0], norm]
                                log.extend(evl)
                                logger.append(log)
        file_operator = TextFileOperator()
        file_operator.writing(logger, logger_path)
        print 'finish'

    def read_article(self, article_path) :
        """ Read source article.
            Each row is an article.
            Colunm[0] is the id of article.
            Column[1:] is the attributes of article.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(article_path)
        entry_list = data_list[0]
        source_list = []
        length = len(data_list[1:]) - 1
        for idx, data in enumerate(data_list[1:]) :
            if len(data) >= len(entry_list) :
                article = dict()
                article['id'] = data[0]
                article['url'] = data[1]
                article['title'] = data[2]
                article['content'] = data[3]
                article['participle_title'] = [Word(word) for word in data[4].split(' ')]
                article['participle_content'] = [Word(word) for word in data[5].split(' ')]
                article['label'] = data[6]
                source_list.append(article)
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        return source_list

    def read_participle(self, articles, participle_path) :
        """ Read participle title.
            Each row is an article.
            Colunm[0] is the id of article.
            Column[1] is the word of participle title.
            Column[2] is the word of participle content.
        """
        file_operator = TextFileOperator()
        data_list = file_operator.reading(participle_path)
        entry_list = data_list[0]
        article_dict = dict()
        length = len(data_list[1:]) - 1
        for idx, data in enumerate(data_list[1:]) :
            if len(data) >= len(entry_list) :
                article = dict()
                article['id'] = data[0]
                article['participle_title'] = [Word(word) for word in data[1].split(' ')]
                article['participle_content'] = [Word(word) for word in data[2].split(' ')]
                article_dict[article['id']] = article
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        length = len(articles) - 1
        for idx, article in enumerate(articles) :
            if article['id'] in article_dict :
                article['participle_title'] = article_dict[article['id']]['participle_title']
                article['participle_content'] = article_dict[article['id']]['participle_content']
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        return articles
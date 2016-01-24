# -*- encoding = gb18030 -*-

# package importing start
import sys
import numpy as np

# import gensim

from basic.word import Word
from file.file_operator import TextFileOperator
from basic.market import PickleMarket, JsonMarket
import classify.selector as selector
from bowlr.classifier import LrClassifier
# package importing end


class Corpus :

    def __init__(self) :
        pass

    def run(self, article_path, article_market_path, dictionary_path, feature_path, \
               feature_market_path, train_path, test_path) :
        """ function for script to drive. """
        # self.run_convert_article(article_path, article_market_path, dictionary_path)
        # self.run_feature_select(article_market_path, dictionary_path, \
                                # feature_path, feature_market_path)
        self.run_classify(train_path, test_path, 'car', 'car')

    def run_convert_article(self,  article_path, article_market_path) :
        articles = self.read_article(article_path)
        loader = PickleMarket()
        loader.dump_market(articles, article_market_path)
        print 'finish.'

    def run_create_dictionary(self, article_market_path, dictionary_path, dict_set) :
        loader = PickleMarket()
        word2id, id2word = dict(), dict()
        index = 0
        for type in dict_set.split('#') :
            path = article_market_path.replace(u'car', type)
            articles = loader.load_market(path)
            length = len(articles) - 1
            for idx, article in enumerate(articles) :
                for word in article['participle_title'] :
                    word =   word.to_string()
                    if word not in word2id :
                        word2id[word] = index
                        id2word[index] = word
                        index += 1
                for word in article['participle_content'] :
                    word = word.to_string()
                    if word not in word2id :
                        word2id[word] = index
                        id2word[index] = word
                        index += 1
                if idx % 100 == 0 :
                    print 'finish rate is %.2f%%\r' % (100.0*idx/length),
            print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        loader = PickleMarket()
        loader.dump_market([word2id, id2word], dictionary_path)

    def run_feature_select(self, article_market_path, dictionary_path, \
                           feature_market_path) :
        loader = PickleMarket()
        articles = loader.load_market(article_market_path)
        [word2id, id2word] = loader.load_market(dictionary_path)
        dim = len(word2id)
        featuresets = list()
        length = len(articles) - 1
        for idx, article in enumerate(articles) :
            feature = [0] * dim
            for word in article['participle_title'] :
                word = word.to_string()
                if word in word2id :
                    feature[word2id[word]] += 1
            for word in article['participle_content'] :
                word = word.to_string()
                if word in word2id :
                    feature[word2id[word]] += 1
            featuresets.append([article['id']] + feature + [article['label']])
            if idx % 100 == 0 :
                print 'finish rate is %.2f%%\r' % (100.0*idx/length),
        print 'finish rate is %.2f%%\r' % (100.0*idx/length)
        file_operator = TextFileOperator()
        # file_operator.writing(featuresets, feature_path)
        loader.dump_market(featuresets, feature_market_path)
        print 'finish'

    def run_classify(self, train_path, test_path, train_set, test_set) :
        loader = PickleMarket()
        # read train
        feature_names = loader.load_market(train_path)[0]
        train_articles = list()
        for type in train_set.split('#') :
            path = train_path.replace(u'car', type)
            train_articles.extend(loader.load_market(path)[1:])
        train_dataset = np.array([np.array(article[1:-1], dtype=float) for article in train_articles])
        print train_dataset.shape
        train_label = np.array([np.array(int(article[-1])) for article in train_articles])
        # read test
        test_articles = list()
        for type in test_set.split('#') :
            path = test_path.replace(u'car', type)
            test_articles.extend(loader.load_market(path)[1:])
        test_dataset = np.array([np.array(article[1:-1]) for article in test_articles])
        print test_dataset.shape
        test_label = np.array([np.array(int(article[-1])) for article in test_articles])
        # train cls
        classifier = LrClassifier()
        train_dataset = classifier.normalize(train_dataset, method='mapminmax')
        test_dataset = classifier.normalize(test_dataset, method='mapminmax')
        classifier.training(train_dataset, train_label, c=10, kernel='linear')
        # test cls
        test_prob = classifier.testing(test_dataset, type='prob')
        test_class = classifier.testing(test_dataset, type='label')
        print 'performance is', classifier.evaluation(test_label, test_prob, test_class)
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
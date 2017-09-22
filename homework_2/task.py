from pattern.web import Wikipedia, plaintext
import re
import string
translator = str.maketrans('', '', string.punctuation)
from nltk import ngrams
import nltk
from nltk.collocations import *
from collections import defaultdict
from nltk.corpus import stopwords as stops
from texttable import Texttable


class WikiParser:
    def __init__(self):
        pass

    def get_articles(self, start):
        corpora = []
        main_article = Wikipedia(language='en').article(start)
        if not main_article:
            return 'Oops - something wrong here. Check if 1) you are trying to access an article from English Wiki; 2) You have not made any typos; 3) Such page exists'
        visited_links = set(main_article.links)
        visited_links.add(main_article.title)
        for article in visited_links:
            try:
                open_article = Wikipedia(language='en').article(article)
                cleaned = open_article.plaintext().translate(translator).lower()
                cleaned = re.sub('\s{2,}', ' ', cleaned)
                corpora.append(cleaned)
            except:
                pass
        return corpora


class TextStatistics:
    def __init__(self, articles):
        self.articles = articles

    def get_top_3grams(self, n):
        tokens = [nltk.word_tokenize(txt) for txt in self.articles]
        flat_tokens = [item for sublist in tokens for item in sublist if not item.isdigit()]
        bgs = nltk.ngrams(flat_tokens, n=3)
        fdist = nltk.FreqDist(bgs)
        ngrams = [ngram for ngram, freq in sorted(fdist.items(), key=lambda item: item[1], reverse=True)][:n]
        freqs = [frq for ngram, frq in sorted(fdist.items(), key=lambda item: item[1], reverse=True)][:n]
        return ngrams, freqs

    def get_top_words(self, n):
        stopwords = ['an', 'with', 'in', 'at', 'near','over','under',
                     'between','among','behind','асrоss','through','to','towards','from',
                     'into','out оf','off','by','for','on','a', 'the', 'of']
        tokens = [nltk.word_tokenize(txt) for txt in self.articles]
        flat_tokens = [item for sublist in tokens for item in sublist if
                       not item.isdigit() and item not in stopwords]
        fdist = nltk.FreqDist(flat_tokens)
        words = [word for word, freq in sorted(fdist.items(), key=lambda item: item[1], reverse=True)][:n]
        freqs = [frq for ngram, frq in sorted(fdist.items(), key=lambda item: item[1], reverse=True)][:n]
        return words, freqs


class Experiment:
    def __init__(self):
        pass

    def show_results(self, parser):
        arts = parser.get_articles('Natural language processing')
        statist = TextStatistics(arts)
        stats_ngrs = statist.get_top_3grams(20)
        stats_words = statist.get_top_words(20)

        nlp = Wikipedia(language='en').article('Natural language processing')
        cleaned = nlp.plaintext().translate(translator).lower()
        cleaned = re.sub('\s{2,}', ' ', cleaned)
        statist_1 = TextStatistics([cleaned])

        stats_ngrs_nlp = statist_1.get_top_3grams(5)
        stats_words_nlp = statist_1.get_top_words(5)

        t1_corpus = Texttable()
        t1_corpus.header(['corpus_3grams', 'freq'])
        for row in zip(stats_ngrs[0], stats_ngrs[1]):
            t1_corpus.add_row(row)


        t2_nlp = Texttable()
        t2_nlp.header(['NLP_3grams', 'freq'])
        for row in zip(stats_ngrs_nlp[0], stats_ngrs_nlp[1]):
            t2_nlp.add_row(row)


        t3_corpus = Texttable()
        t3_corpus.header(['corpus_top_words', 'freq'])
        for row in zip(stats_words[0], stats_words[1]):
            t3_corpus.add_row(row)

        t4_nlp = Texttable()
        t4_nlp.header(['NLP_top_words', 'freq'])
        for row in zip(stats_words_nlp[0], stats_words_nlp[1]):
            t4_nlp.add_row(row)


        print(t1_corpus.draw())
        print(t2_nlp.draw())
        print(t3_corpus.draw())
        print(t4_nlp.draw())


#
# pars = WikiParser()
# experiment = Experiment()
# experiment.show_results(pars)
#
# +---------------------------------------+------+
# |             corpus_3grams             | freq |
# +=======================================+======+
# | ('from', 'the', 'original')           | 280  |
# +---------------------------------------+------+
# | ('archived', 'from', 'the')           | 271  |
# +---------------------------------------+------+
# | ('natural', 'language', 'processing') | 241  |
# +---------------------------------------+------+
# | ('the', 'original', 'on')             | 217  |
# +---------------------------------------+------+
# | ('the', 'use', 'of')                  | 215  |
# +---------------------------------------+------+
# | ('as', 'well', 'as')                  | 192  |
# +---------------------------------------+------+
# | ('one', 'of', 'the')                  | 165  |
# +---------------------------------------+------+
# | ('cambridge', 'university', 'press')  | 152  |
# +---------------------------------------+------+
# | ('a', 'b', 'c')                       | 149  |
# +---------------------------------------+------+
# | ('the', 'european', 'union')          | 145  |
# +---------------------------------------+------+
# | ('proceedings', 'of', 'the')          | 140  |
# +---------------------------------------+------+
# | ('such', 'as', 'the')                 | 135  |
# +---------------------------------------+------+
# | ('university', 'press', 'isbn')       | 134  |
# +---------------------------------------+------+
# | ('of', 'the', 'european')             | 133  |
# +---------------------------------------+------+
# | ('the', 'number', 'of')               | 132  |
# +---------------------------------------+------+
# | ('a', 'number', 'of')                 | 122  |
# +---------------------------------------+------+
# | ('for', 'example', 'the')             | 121  |
# +---------------------------------------+------+
# | ('a', 'set', 'of')                    | 119  |
# +---------------------------------------+------+
# | ('based', 'on', 'the')                | 108  |
# +---------------------------------------+------+
# | ('in', 'order', 'to')                 | 102  |
# +---------------------------------------+------+
# +---------------------------------------+------+
# |              NLP_3grams               | freq |
# +=======================================+======+
# | ('natural', 'language', 'processing') | 12   |
# +---------------------------------------+------+
# | ('chunk', 'of', 'text')               | 6    |
# +---------------------------------------+------+
# | ('a', 'chunk', 'of')                  | 6    |
# +---------------------------------------+------+
# | ('of', 'natural', 'language')         | 5    |
# +---------------------------------------+------+
# | ('the', 'complexity', 'of')           | 4    |
# +---------------------------------------+------+
# +------------------+-------+
# | corpus_top_words | freq  |
# +==================+=======+
# | and              | 14127 |
# +------------------+-------+
# | is               | 7527  |
# +------------------+-------+
# | as               | 4876  |
# +------------------+-------+
# | that             | 4185  |
# +------------------+-------+
# | are              | 3756  |
# +------------------+-------+
# | or               | 3202  |
# +------------------+-------+
# | language         | 3174  |
# +------------------+-------+
# | be               | 2922  |
# +------------------+-------+
# | it               | 2309  |
# +------------------+-------+
# | this             | 2110  |
# +------------------+-------+
# | which            | 1894  |
# +------------------+-------+
# | can              | 1809  |
# +------------------+-------+
# | not              | 1781  |
# +------------------+-------+
# | retrieved        | 1547  |
# +------------------+-------+
# | was              | 1536  |
# +------------------+-------+
# | such             | 1531  |
# +------------------+-------+
# | have             | 1477  |
# +------------------+-------+
# | english          | 1476  |
# +------------------+-------+
# | also             | 1469  |
# +------------------+-------+
# | words            | 1438  |
# +------------------+-------+
# +---------------+------+
# | NLP_top_words | freq |
# +===============+======+
# | and           | 70   |
# +---------------+------+
# | language      | 53   |
# +---------------+------+
# | is            | 47   |
# +---------------+------+
# | natural       | 33   |
# +---------------+------+
# | as            | 30   |
# +---------------+------+
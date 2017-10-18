from pattern.web import Wikipedia, plaintext
import re
import string
from nltk.tokenize import sent_tokenize
translator = str.maketrans('', '', string.punctuation)
from nltk import ngrams
import nltk
from nltk.collocations import *
from collections import defaultdict
from nltk.corpus import stopwords as stops
from texttable import Texttable
import math
import unittest

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
                cleaned = open_article.plaintext().lower()
                cleaned = re.sub('\s{2,}', ' ', cleaned)
                corpora.append(cleaned)
            except:
                pass
        return corpora


class TextStatistics:
    def __init__(self, articles):
        self.articles = articles

    def get_top_3grams(self, n, use_idf=False):
        all_sentences = []
        for art in self.articles:
            all_sentences += sent_tokenize(art)
        n_of_sentences = len(all_sentences)
        # print(all_sentences)
        # letter_tokens = []
        # for txt in self.articles:
            # letter_tokens.append(list(txt.translate(translator)))
        # print(letter_tokens)
        bgs = []
        for sent in all_sentences:
            bgs_arr = nltk.ngrams(sent, n=3)
            for i in bgs_arr:
                if not any([char in string.punctuation for char in i]):
                    bgs.append(i)
            # bgs+=bgs_arr

        fdist = nltk.FreqDist(bgs)
        # print(fdist)
        if use_idf:
            for tri in fdist.keys():
                # print(tri)
                count_tri = 0
                for sent in all_sentences:
                    # print(sent.count(''.join(tri)))
                    if ''.join(tri) in sent:
                        count_tri+=1

                tri_tfidf = math.log10(n_of_sentences/count_tri)
                fdist[tri] = fdist[tri] * tri_tfidf

        ngrams = [ngram for ngram, freq in sorted(fdist.items(), key=lambda item: (-item[1], item[0]))][:n]
        # print(ngrams)
        freqs = [frq for ngram, frq in sorted(fdist.items(), key=lambda item: (-item[1], item[0]))][:n]
        # print(freqs)
        return ngrams, freqs

    def get_top_words(self, n, use_idf=False):
        len_corpus = len(self.articles)
        stopwords = ['an', 'with', 'in', 'at', 'near','over','under',
                     'between','among','behind','асrоss','through','to','towards','from',
                     'into','out оf','off','by','for','on','a', 'the', 'of']
        tokens = [nltk.word_tokenize(txt) for txt in self.articles]
        # print(len_corpus)
        # print(tokens)
        flat_tokens = [item for sublist in tokens for item in sublist if
                       not item.isdigit() and item not in stopwords]
        fdist = nltk.FreqDist(flat_tokens)
        # print(fdist.items())
        # print(fdist.items())
        if use_idf:
            for word in fdist.keys():
                count_art = 0
                for tok in tokens:
                    if word in tok:
                        count_art+=1

                word_tfidf = math.log10(len_corpus/count_art)
                # print(count_art)
                fdist[word] = fdist[word]*word_tfidf

        words = [word for word, freq in sorted(fdist.items(), key=lambda item: (-item[1], item[0]))][:n]
        # print(words)
        freqs = [frq for ngram, frq in sorted(fdist.items(), key=lambda item: (-item[1], item[0]))][:n]
        # print(freqs)
        return words, freqs


class Experiment:
    def __init__(self):
        pass

    def show_results(self, parser):
        arts = parser.get_articles('Natural language processing')
        statist = TextStatistics(arts)
        stats_ngrs = statist.get_top_3grams(30, use_idf=True)
        stats_words = statist.get_top_words(20, use_idf=True)

        # nlp = Wikipedia(language='en').article('')
        # cleaned = nlp.plaintext().translate(translator).lower()
        # cleaned = re.sub('\s{2,}', ' ', cleaned)
        # statist_1 = TextStatistics([cleaned])

        # stats_ngrs_nlp = statist_1.get_top_3grams(5)
        # stats_words_nlp = statist_1.get_top_words(5)

        t1_corpus = Texttable()
        t1_corpus.header(['corpus_3grams', 'freq'])
        for row in zip(stats_ngrs[0], stats_ngrs[1]):
            t1_corpus.add_row(row)


        # t2_nlp = Texttable()
        # t2_nlp.header(['NLP_3grams', 'freq'])
        # for row in zip(stats_ngrs_nlp[0], stats_ngrs_nlp[1]):
        #     t2_nlp.add_row(row)


        t3_corpus = Texttable()
        t3_corpus.header(['corpus_top_words', 'freq'])
        for row in zip(stats_words[0], stats_words[1]):
            t3_corpus.add_row(row)

        # t4_nlp = Texttable()
        # t4_nlp.header(['NLP_top_words', 'freq'])
        # for row in zip(stats_words_nlp[0], stats_words_nlp[1]):
        #     t4_nlp.add_row(row)


        print(t1_corpus.draw())
        # print(t2_nlp.draw())
        print(t3_corpus.draw())
        # print(t4_nlp.draw())



# pars = WikiParser()
# experiment = Experiment()
# experiment.show_results(pars)



class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_tfidfs_words(self):
        stats = TextStatistics(['i am a student', 'i am a dog', 'i am running', 'i']).get_top_words(5, True)
        self.assertListEqual(stats[0], ['dog', 'running', 'student', 'am', 'i'])
        self.assertListEqual(stats[1], [0.6020599913279624, 0.6020599913279624, 0.6020599913279624, 0.3748162098248998, 0.0])

    def test_tfidfs_3grams(self):
        stats = TextStatistics(['sent a', 'sent b']).get_top_3grams(5, True)
        self.assertListEqual(stats[0], [('t', ' ', 'a'), ('t', ' ', 'b'), ('e', 'n', 't'), ('n', 't', ' '), ('s', 'e', 'n')])
        self.assertListEqual(stats[1], [0.3010299956639812, 0.3010299956639812, 0.0, 0.0, 0.0])



case = TestCase()
suite = unittest.TestLoader().loadTestsFromModule(case)
unittest.TextTestRunner().run(suite)

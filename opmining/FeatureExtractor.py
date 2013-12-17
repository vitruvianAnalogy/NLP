#!/usr/bin/python2.7

from POSTagger import POSTagger
from Tokenizer import Tokenizer
from nltk import FreqDist
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet

class FeatureExtractor:
    """Extracts the Frequent Features of the Products by Mining the Reviews - Uses Apriori Algorithm"""

    def __init__(self,total_content):
        self.candidate_features = []
        self.feature_sentences = []
        self.init_feature_sentences(total_content)

    def get_stopwords(self):
        words = stopwords.words('english')
        #Find a way to eliminate the need for adding custom stopwords
        words.extend(['pros', 'cons', 'things', 'day', 'points', 'time', 'month', 'year','tablet', 'lot', 'iphone',
                      'problem', 'apple', 'product', 'item', 'computer', 'laptop', 'feature', 'way', 'everything',
                      'thing', 'work'])
        return words

    def init_feature_sentences(self, total_content):
        t = Tokenizer()
        p = POSTagger()
        wnl = WordNetLemmatizer()

        sentences = t.sent_tokenize(total_content.lower())

        for sentence in sentences:
            tagged_sentence = p.ntlk_tag(t.word_tokenize(sentence))

            #Initializing Feature Sentence dictionary
            feature_sentence = {}
            feature_sentence['sentence'] = sentence
            feature_sentence['tags'] = tagged_sentence
            feature_sentence['nouns'] = []
            feature_sentence['noun_phrases'] = []

            #Finding the Nouns/Noun Phrases in the tagged sentence
            for i in range(0,len(tagged_sentence)):
                (word, tag) = tagged_sentence[i]

                #Chunking
                if tag.startswith('N') and tag != 'NNP':
                    if i > 0 and len(feature_sentence['nouns']) > 0 and tagged_sentence[i - 1][0] == feature_sentence['nouns'][-1] and feature_sentence['sentence'].find(feature_sentence['nouns'][-1] + ' ' + word) > -1:
                        feature_sentence['noun_phrases'].append(wnl.lemmatize(feature_sentence['nouns'].pop() + ' ' + word))
                    else:
                        feature_sentence['nouns'].append(wnl.lemmatize(word))

            self.feature_sentences.append(feature_sentence)

    def get_candidate_feature_list(self):
        for feature_sentence in self.feature_sentences:
            self.candidate_features.extend(list(set(feature_sentence['nouns'])))
            self.candidate_features.extend(list(set(feature_sentence['noun_phrases'])))
        return self.candidate_features

    def prune_features(self, features, p_support):
        #The most frequent feature is the type of product (from many observations)
        self.product_name = features.pop(0)[0]

        #Find a way to eliminate the need for adding custom words
        words = self.get_stopwords()
        #Eliminate words that represent the name of the product
        words.extend(self.product_name)

        features = filter(lambda x: len(x[0]) > 2 and x[0] not in words, features)

        #print features

        #Map 1 word features to their supersets (Eg. battery to battery life)
        for i in xrange(0, len(features)):
            for j in xrange(0, len(features)):
                if features[i][0] in features[j][0].split():
                    features[i] = features[j]

        return sorted(list(set(features)), key=lambda x: x[1], reverse=True )

    def get_frequent_features_list(self, min_support):
        dist = FreqDist(self.get_candidate_feature_list())
        features = [(item, count) for (item, count) in dist.iteritems() if count >= min_support]
        return self.prune_features(features, 3)



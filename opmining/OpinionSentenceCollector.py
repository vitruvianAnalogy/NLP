from nltk.corpus import WordListCorpusReader

class OpinionSentenceCollector:
    def __init__(self, features, feature_sentences):
        self.features = features
        self.feature_sentences = feature_sentences
        self.opinion_sentences = []
        self.opinion_features = []

        self.init_corpus()

        for sentence_index in xrange(len(self.feature_sentences)):
            sentence = self.feature_sentences[sentence_index]
            self.feature_sentences[sentence_index]['opinion_sentence'] = []
            for feature in self.features:
                #Extracting the feature from (feature, count) tuple
                feature = feature[0]
                if feature in sentence['nouns'] or feature in sentence['noun_phrases']:
                    for tag_index in xrange(len(sentence['tags'])):
                        (word, tag) = sentence['tags'][tag_index]
                        if(word.find(feature.split()[0])) > -1:
                            (sentiment_score, opinion) = self.calculate_sent_score(sentence['tags'], tag_index)
                            if len(opinion) > 0:
                                self.opinion_features.append(feature)
                                self.opinion_sentences.append((feature, sentiment_score, sentence['sentence']))

    def init_corpus(self):
        self.negation_words = WordListCorpusReader('../data/corpus/', 'negation-words.txt')
        self.negative_sentiments = WordListCorpusReader('../data/corpus/', 'negative-words.txt')
        self.positive_sentiments = WordListCorpusReader('../data/corpus/', 'positive-words.txt')


    def calculate_sent_score(self, tags, tag_index):

        positive_sentiment_score = 0
        negative_sentiment_score = 0
        adjective = ''
        negation_words = ''

        for i in xrange(tag_index + 1, len(tags)):
            (word, tag) = tags[i]
            if word in self.negation_words.words():
                negation_words = word
            if tag in ['JJ', 'JJR', 'JJS']:
                adjective = word
                if word in self.negative_sentiments.words():
                    adjective = word
                    if not len(negation_words) > 0:
                        negative_sentiment_score += 1
                    else:
                        positive_sentiment_score += 1
                if word in self.positive_sentiments.words():
                    adjective = word
                    if not len(negation_words) > 0:
                        positive_sentiment_score += 1
                    else:
                        negative_sentiment_score += 1

        start = 0
        negation_words = ''

        for j in xrange(start, tag_index):
            (word, tag) = tags[j]
            if word in self.negation_words.words():
                negation_words = word
            if tag in ['JJ', 'JJR', 'JJS']:
                adjective = word
                if word in self.negative_sentiments.words():
                    adjective = word
                    if not len(negation_words) > 0:
                        negative_sentiment_score += 1
                    else:
                        positive_sentiment_score += 1
                if word in self.positive_sentiments.words():
                    if not len(negation_words) > 0:
                        positive_sentiment_score += 1
                    else:
                        negative_sentiment_score += 1

        final_score = positive_sentiment_score - negative_sentiment_score

        #print "Sentiment Score", final_score, adjective
        return final_score, adjective







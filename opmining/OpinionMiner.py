#!/usr/bin/env python
from ReviewsExtractor import ReviewsExtractor
from FeatureExtractor import FeatureExtractor
from OpinionSentenceCollector import OpinionSentenceCollector
import sys,pprint


class OpinionMiner:
    def __init__(self, min_support=20):
        self.min_support = min_support
        self.features = []
        self.ratings = {}
        self.sorted_features = []
        self.final_features = []

    def run(self):

        #Calling the ReviewsExtractor class to read the csv file
        #and extract,concatenate the reviews
        rev = ReviewsExtractor()
        rev.extract_review_content()
        total_content = rev.get_concatenated_reviews()

        f = FeatureExtractor(total_content)

        self.features = f.get_frequent_features_list(self.min_support)

        o = OpinionSentenceCollector(self.features, f.feature_sentences)

        for feature in o.opinion_features:
            self.ratings[feature] = {'positive': 0, 'negative': 0, 'neutral': 0, 'total_reviews': 0, 'negative_review': '', 'positive_review': ''}

        for feature, sentiment_score, sentence in o.opinion_sentences:
            self.ratings[feature]['total_reviews'] += 1
            if sentiment_score > 0:
                self.ratings[feature]['positive'] += 1
                self.ratings[feature]['positive_review'] = sentence
            elif sentiment_score < 0:
                self.ratings[feature]['negative'] += 1
                self.ratings[feature]['negative_review'] = sentence
            else:
                self.ratings[feature]['neutral'] += 1

        for feature in o.opinion_features:
            self.final_features.append((feature,self.ratings[feature]['total_reviews']))

        self.sorted_features = sorted(set(self.final_features), key=lambda x: x[1], reverse=True)

        pp = pprint.PrettyPrinter(indent=4)

        print self.sorted_features
        print len(self.sorted_features)

        for index in range(0, 10):
            iter_feature = self.sorted_features[index][0]
            print "Feature: ", iter_feature
            pp.pprint(self.ratings[iter_feature])


def main():
    om = OpinionMiner()
    om.run()


if __name__ == '__main__':
    main()

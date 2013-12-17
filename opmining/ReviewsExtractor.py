#!/usr/bin/python

import csv
import properties


class ReviewsExtractor:

    def __init__(self):
        self.reviews_csv_path = properties.reviews_csv_path
        self.reviews = []

    def extract_review_content(self):
        csv_file = open(self.reviews_csv_path, "rb")
        csv_reader = csv.reader(csv_file)
        self.reviews = [{'title': review[8], 'content': review[9]} for review in csv_reader]
        csv_file.close()

    def get_concatenated_reviews(self):
        if self.reviews:
            return "".join([review['content'] for review in self.reviews])
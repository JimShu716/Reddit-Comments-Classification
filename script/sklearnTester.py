# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 18:35:03 2019

@author: sunge
"""
import nltk
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import string
from tqdm import tqdm
from numpy import transpose as T
from scipy.stats import stats
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from nltk.stem.snowball import SnowballStemmer
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

#---------------------------------------------------------------------------
#X = [[0,0],[1,1]]
#Y = [0,1]
#clf = tree.DecisionTreeClassifier()
#clf = clf.fit(X,Y)
#print(clf.predict([[2.,2.]]))
#------------------------------------------------------------------
def encode_subreddit(argument):
    switch = {
           "hockey":0,
            "nba":1,
            "leagueoflegends":2,
            "soccer":3,
            "funny":4,
            "movies":5,
            "anime":6,
            "Overwatch":7,
            "trees":8,
            "GlobalOffensive":9,
            "nfl":10,
            "Askreddit":11,
            "gameofthrones":12,
            "conspiracy":13,
            "worldnews":14,
            "wow":15,
            "europe":16,
            "canada":17,
            "Music":18,
            "baseball":19,             
            }
    return switch.get(argument,20)
#------------------------------------------------------------------------------
#encode subreddit

encode = []
training_data_df = pd.read_csv('../data/original_data/reddit_train.csv')
for subreddit in training_data_df['subreddits']:
    encode.append(encode_subreddit(subreddit))
training_data_df['subreddit_encoding'] = encode

#tokenize
#------------------------------------------------------------------------------   
count_vect = CountVectorizer()
train_counts = count_vect.fit_transform(training_data_df['comments'][20000:])
print(train_counts.shape)

#tf idf
#------------------------------------------------------------------------------
tfidf_transformer = TfidfTransformer()
train_tfidf = tfidf_transformer.fit_transform(train_counts)
print(train_tfidf.shape)

#train model
#------------------------------------------------------------------------------
clf = MultinomialNB().fit(train_tfidf,training_data_df['subreddit_encoding'][20000:])
testing_count = count_vect.transform(training_data_df['comments'][:20000])
testing_tfidf = tfidf_transformer.transform(testing_count)
predicted = clf.predict(testing_tfidf)

#calculate accuracy
#------------------------------------------------------------------------------
accuracy = 0
index = 0
for result in predicted:
    if result == training_data_df['subreddit_encoding'][index]:
          #  print("true",training_data_df['subreddit_encoding'][index])
        #    print("predict",result)
         #   print("------------")
         accuracy+=1
    index+=1






















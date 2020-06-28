import twitter_sentiment as ts

import re
import pandas as pd
import time
import nltk
from nltk.tokenize import word_tokenize
from string import punctuation 
from nltk.corpus import stopwords 

def get_training_data(filename='corpus.csv'):
    '''
    '''
    df = pd.read_csv('corpus.csv', names=['Handle','Sentiment','ID', 'Tweet'])
    neo = ts.MrAnderson()
    for i, row in df.iterrows():
        try:
            neo.get_by_id(row['ID'])
            df['Tweet'][i] = neo.tweet.text
            print(f'{i} {id} successful')
        except:
            print(f'{i} {id} not successful')
            continue
    return df



class PreProcessTweets:
    '''
    '''
    def __init__(self):
        self._stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER','URL'])

    def get_data(self, filename='training.csv'):
        df = pd.read_csv(filename)
        df = df.dropna()
        # remove null entries
        print(df.head())
        
    def processTweets(self, list_of_tweets):
        processedTweets=[]
        for tweet in list_of_tweets:
            processedTweets.append((self._processTweet(tweet["text"]),tweet["label"]))
        return processedTweets
    
    def _processTweet(self, tweet):
        tweet = tweet.lower() # convert text to lower-case
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet) # remove URLs
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet) # remove usernames
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet) # remove the # in #hashtag
        tweet = word_tokenize(tweet) # remove repeated characters (helloooooooo into hello)
        return [word for word in tweet if word not in self._stopwords]

if __name__ == '__main__':
    n = PreProcessTweets()
    n.get_data()
import twitter_sentiment as ts

import re
import pandas as pd
import time
import nltk
from nltk.tokenize import word_tokenize
from string import punctuation 
from nltk.corpus import stopwords 
import pickle


def download_training_data(filename='corpus.csv'):
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
        self.get_data()

    def get_data(self, filename='training.csv'):
        df = pd.read_csv(filename)
        self.trainingSetRaw = df.dropna().head()
        
    def processTweets(self):
        processedTweets=[]
        for i, tweet in self.trainingSetRaw.iterrows():
            processedTweets.append((self._processTweet(tweet["Tweet"]),tweet["Sentiment"]))
        self.trainingSetProcessed = processedTweets

    def buildTrainingSet(tweets):
        processedTweets=[]
        for tweet in tweets:
            processedTweets.append(self._processTweet(tweet),None)
        return processedTweets
    
    def _processTweet(self, tweet):
        tweet = tweet.lower() # convert text to lower-case
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet) # remove URLs
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet) # remove usernames
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet) # remove the # in #hashtag
        tweet = word_tokenize(tweet) # remove repeated characters (helloooooooo into hello)
        return [word for word in tweet if word not in self._stopwords]

    def buildVocabulary(self):
        def extract_features(tweet):
            tweet_words = set(tweet)
            features = {}
            for word in self.wordFeatures:
                features['contains(%s)' % word] = (word in tweet_words)
            return features 

        all_words = []
        for (words, sentiment) in self.trainingSetProcessed:
            all_words.extend(words)
        self.wordList = nltk.FreqDist(all_words)
        self.wordFeatures = self.wordList.keys()
        self.trainingFeatures = nltk.classify.apply_features(extract_features, self.trainingSetProcessed)

    def naiveBayes(self):
        self.NB = nltk.NaiveBayesClassifier.train(self.trainingFeatures)
        return self.NB

    def saveModel(self, model, filename='model'):
        f = open(filename, 'wb')
        pickle.dump(model, f)
        f.close()

    def loadModel(self, filename='model.pickle'):
        f = open(filename, 'rb')
        model = pickle.load(f)
        f.close()
        return model

if __name__ == '__main__':
    n = PreProcessTweets()
    model = n.loadModel()
    
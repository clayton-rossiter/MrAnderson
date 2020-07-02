import twitter_scraper as ts
import preprocess as pp

import re
import pandas as pd
import time
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation 
from nltk.corpus import stopwords 
import pickle


def download_training_data(filename='corpus.csv'):
    '''
    '''
    df = pd.read_csv('corpus.csv', names=['handle','sentiment','id','tweet'])
    neo = ts.MrAnderson()
    for i, row in df.iterrows():
        try:
            neo.get_by_id(row['id'])
            df['tweet'][i] = neo.tweet.text
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
        self.processTweets()
        self.buildVocabulary()

    def get_data(self, filename='training.csv', shuffle=True, trainSplit=0.8):
        '''

        '''
        df = pd.read_csv(filename)
        # by default, shuffle training dataset
        if trainSplit < 1:
            df = df[:int(len(df)*trainSplit)]
        if shuffle == True:
            self.trainingSetRaw = df.dropna().sample(frac=1).reset_index(drop=True)
        else:
            self.trainingSetRaw = df.dropna()
        
    def processTweets(self):
        processedTweets=[]
        for i, tweet in self.trainingSetRaw.iterrows():
            processedTweets.append((self._processTweet(tweet["tweet"]),tweet["sentiment"]))
        self.trainingSetProcessed = processedTweets

    def buildTestSet(self, tweets):
        processedTweets=[]
        try:
            for tweet in tweets:
                processedTweets.append((self._processTweet(tweet),None))
            return processedTweets
        except:
            print("Unfortunately, something went wrong...")
            return None
    
    def _processTweet(self, tweet):
        # tweet = tweet.lower() # convert text to lower-case
        # tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet) # remove URLs
        # tweet = re.sub('@[^\s]+', 'AT_USER', tweet) # remove usernames
        # tweet = re.sub(r'#([^\s]+)', r'\1', tweet) # remove the # in #hashtag
        # tweet = word_tokenize(tweet) # remove repeated characters (helloooooooo into hello)
        tweet = pp.total_preprocess(tweet)
        return [word for word in tweet if word not in self._stopwords]

    def buildVocabulary(self):
        all_words = []
        for (words, sentiment) in self.trainingSetProcessed:
            all_words.extend(words)
        self.wordList = nltk.FreqDist(all_words)
        self.wordFeatures = self.wordList.keys()
        self.trainingFeatures = nltk.classify.apply_features(self.extract_features, self.trainingSetProcessed)
        

    def extract_features(self, tweet):
        tweet_words = set(tweet)
        features = {}
        for word in self.wordFeatures:
            features['contains(%s)' % word] = (word in tweet_words)
        return features

    def naiveBayes(self):
        self.NB = nltk.NaiveBayesClassifier.train(self.trainingFeatures)
        return self.NB

    def classify(self, testSet, model):
        results = [model.classify(self.extract_features(tweet[0])) for tweet in testSet]
        self.results = results
        return results

    def saveModel(self, model, filename='model.pickle'):
        f = open(filename, 'wb')
        pickle.dump(model, f)
        f.close()

    def loadModel(self, filename='model.pickle'):
        f = open(filename, 'rb')
        model = pickle.load(f)
        f.close()
        return model

if __name__ == '__main__':
    # get training tweets
    neo = ts.MrAnderson()
    neo.search('puppy')
    
    # create and train model
    # n = PreProcessTweets()
    # model = n.naiveBayes()
    # n.saveModel(model)

    # test new dataset against model
    n = PreProcessTweets()
    # model = n.loadModel()
    # testSet = n.buildTestSet(neo.df['tweet'].tolist())
    # n.buildVocabulary()
    # results = n.classify(testSet,model)
    # for result, tweet in zip(results, testSet):
    #     print(result, tweet)
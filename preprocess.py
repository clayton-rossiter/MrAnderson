import twitter_scraper as ts

import regex as re
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from string import punctuation


# Program constants
POSITIVE_WORD_LIBRARY = list(set(open('words/positive.txt').read().split()))
NEGATIVE_WORD_LIBRARY = list(set(open('words/negative.txt').read().split()))
STOPWORDS = set(stopwords.words('english') + list(punctuation) + ['AT_USER','URL'])


def abbreviation_replacement(text):
    '''
    purpose:        take plain text and turn all abbreviations into proper words
                    e.g. he's = he is, what's = what is
                    also adds spaces to any punctuation to allow tokenization
    inputs:         string  (tweet)
    outputs:        string  (tweet) amended
    '''
    text = re.sub(r"i\'m", "i am", text)
    text = re.sub(r"\'re", "are", text)
    text = re.sub(r"he\'s", "he is", text)
    text = re.sub(r"it\'s", "it is", text)
    text = re.sub(r"that\'s", "that is", text)
    text = re.sub(r"who\'s", "who is", text)
    text = re.sub(r"what\'s", "what is", text)
    text = re.sub(r"n\'t", "not", text)
    text = re.sub(r"\'ve", "have", text)
    text = re.sub(r"\'d", "would", text)
    text = re.sub(r"\'ll", "will", text)
    text = re.sub(r",", " , ", text)
    text = re.sub(r"!", " ! ", text)
    text = re.sub(r"\.", " \. ", text)
    text = re.sub(r"\?", " \? ", text)
    # text = re.sub(r"\(", " \( ", text)
    # text = re.sub(r"\)", " \) ", text)
    return text

def emoji_translation(text):
    '''
    purpose:        take classic emojis and add a positive/negative/neutral emphasis to these
                    example:    8=) will be considered a happy smiley
                                :( will be considered a negative smiley
    inputs:         string  (tweet)
    outputs:        string  (tweet) with sentiment emphasis
    '''
    loves = ["<3", "♥"]
    smilefaces = []
    sadfaces = []
    neutralfaces = []

    eyes = ["8",":","=",";"]
    nose = ["'","`","-",r"\\"]
    for e in eyes:
        for n in nose:
            for s in [")", "d", "]", "}","p"]:
                smilefaces.append(e+n+s)
                smilefaces.append(e+s)
            for s in ["(", "[", "{"]:
                sadfaces.append(e+n+s)
                sadfaces.append(e+s)
            for s in ["|", "/", r"\\"]:
                neutralfaces.append(e+n+s)
                neutralfaces.append(e+s)
            #reversed
            for s in ["(", "[", "{"]:
                smilefaces.append(s+n+e)
                smilefaces.append(s+e)
            for s in [")", "]", "}"]:
                sadfaces.append(s+n+e)
                sadfaces.append(s+e)
            for s in ["|", "/", r"\\"]:
                neutralfaces.append(s+n+e)
                neutralfaces.append(s+e)

    smilefaces = list(set(smilefaces))
    sadfaces = list(set(sadfaces))
    neutralfaces = list(set(neutralfaces))

    t = []
    for w in text.split():
        if w in loves:
            t.append("<love>")
        elif w in smilefaces:
            t.append("<happy>")
        elif w in neutralfaces:
            t.append("<neutral>")
        elif w in sadfaces:
            t.append("<sad>")
        else:
            t.append(w)
    newText = " ".join(t)
    return newText

def neaten_tweet(tweet):
    newTweet = tweet
    newTweet = newTweet.lower() # convert text to lower-case
    newTweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', newTweet) # remove URLs
    newTweet = re.sub('@[^\s]+', 'AT_USER', newTweet) # remove usernames
    newTweet = re.sub(r'#([^\s]+)', r'\1', newTweet) # remove the # in #hashtag
    return newTweet

def emphasize_pos_and_neg_words(text):
    '''
    purpose:        Takes dictionary (From Kaggle) of positive and negative words and cross-checks
                    Tweets against these, adds emphasis to tweet and returns new string
    inputs:         string  (tweet)
    outputs:        string  (tweet) original tweet with positive/negative emphasis
    '''
    t = []
    for w in text.split():
        if w in POSITIVE_WORD_LIBRARY:
            t.append('<positive> ' + w)
        elif w in NEGATIVE_WORD_LIBRARY:
            t.append('<negative> ' + w)
        else:
            t.append(w)
    newTweet = " ".join(t)
    return newTweet

def separate(tweet):
    '''
    purpose:        Takes a string sentence and converts it into a tokenized list for nltk 
                    analysis, while removing any nltk.corpus stopwords
    inputs:         string  (tweet)
    outputs:        list    (tweet)
    '''
    tweet = word_tokenize(tweet)
    return [word for word in tweet if word not in STOPWORDS]

def tag_words(tweet, allow=['JJ']):
    '''
    purpose:        using the nltk pos_tag, tag each word with their likely association, e.g. noun,
                    adjective, verb etc.
    inputs:         string (tweet)
                    allow       default ['JJ']
                    define which types of words to permit, by default only permit adjectives
                    further information can be found at https://www.nltk.org/book/ch05.html
    outputs:        list of tuples [(word, association)]
    '''
    tagged = pos_tag(tweet)
    newTweet=[]
    for tag in tagged:
        if tag[1] in allow:
            newTweet.append(tag[0])
    return newTweet

def stem(tweet):
    '''
    purpose:
    inputs:
    outputs:
    '''
    stemmer = SnowballStemmer("english")
    # for word in tweet:
    #     newTweet = 
    return stemmer.stem(tweet)




def total_preprocess(tweet):
    newTweet = tweet
    newTweet = abbreviation_replacement(newTweet)
    newTweet = neaten_tweet(newTweet)
    newTweet = emoji_translation(newTweet)
    newTweet = emphasize_pos_and_neg_words(newTweet)
    newTweet = separate(newTweet)
    newTweet = tag_words(newTweet)
    return newTweet

# if __name__ == '__main__':
#     # tweets = [
#     #     r"Absolutely hating this new game :(!",
#     #     r":) loving that he's in the new movie!"
#     # ]
#     neo = ts.MrAnderson()
#     neo.search("puppy")
#     tweets = neo.df['tweet'].tolist()
#     # newTweets = total_preprocess(tweets)
#     newTweets = []
#     for tweet in tweets:
#         tweet = total_preprocess(tweet)
#         newTweets.append(tweet)
#     for old, new in zip(tweets,newTweets):
#         print(old,new)
    
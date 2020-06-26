# secret keys etc.
import secret_stuff
# libraries
import re
import tweepy as tw
import pandas as pd


class MrAnderson():
    def __init__(self):
        self.connect()

    def connect(self):
        '''
        purpose:    use secret API keys to log into Twitter and store search API
        inputs:     secret keys from external file
        outputs:    None
        '''
        auth = tw.OAuthHandler(secret_stuff.consumer_key, secret_stuff.consumer_secret)
        auth.set_access_token(secret_stuff.access_token_key, secret_stuff.access_token_secret)
        self.api = tw.API(auth, wait_on_rate_limit=True)

    def search(self, hashtag, search_after='2020-01-01', limit=None, as_dataframe=True,\
        filter_retweet=True):
        '''
        purpose:    means to search twitter for hashtag tweets
        inputs:     hashtag:        hashtag string to search for
                    search_after:   default: 1st January 2020 ('2020-01-01')
                                    date in YYYY-MM-DD format
                    limit:          default:None
                                    limit number of items returned
                    as_dataframe:   default:True
                                    whether to return as pandas dataframe
                    filter_retweet: default:True
                                    filter retweets from results
        outputs:    pd.DataFrame/List of tweets from search terms
        '''
        # check data types are correct and store last searched terms
        # hashtag
        if not isinstance(hashtag,str):
            print("Ensure search term is a string!")
            return
        else:
            if hashtag[0] != '#':
                self.hashtag = ''.join(('#',hashtag.strip()))
            else:
                self.hashtag = hashtag
        # search_after
        if not isinstance(search_after,str):
            print('Ensure search_after is a string!')
            return
        else:
            if not re.match(r'\d{4}-\d{2}-\d{2}', search_after):
                print('Ensure search_after is in YYYY-MM-DD format!')
                return
            else:
                self.search_after = search_after

        # run search function using Cursor
        self.tweets = tw.Cursor(
            self.api.search,
            q = hashtag + '-filter:retweets',
            lang="en",
            since=search_after,
            tweet_mode='extended'
        ).items(10)
        # get necessary data into columns
        data = [[tweet.user.screen_name, tweet.user.location, tweet.full_text] for tweet in self.tweets]
        self.df = pd.DataFrame(data=data, columns=['user','location','tweet'])

    def export(self, filename=None):
        '''
        purpose:    export saved search results to a csv file in current directory
        inputs:     must have previously run search (error raise)
                    must be a pandas dataframe
        outputs:    results.csv in current
        '''
        # check there are results, and check it's a dataframe
        try:
            if not isinstance(self.df, pd.DataFrame):
                print("Ensure to search and save as a pandas dataframe!")
                return
        except:
            print("Ensure you have searched for a tweet!")
            return
        # export to csv
        if filename != None:
            filename = f'tweets_{self.hashtag}{self.search_after}.csv'
        self.df.to_csv(filename)


if __name__ == '__main__':
    neo = MrAnderson()
    neo.search('blm','2020-06-01')
    
# secret keys etc.
import secret_stuff
# libraries
import tweepy as tw
import re

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

    def search(self, hashtag, search_after, limit=None, as_dataframe=True,\
        filter_retweet=True):
        '''
        purpose:    means to search twitter for hashtag tweets
        inputs:     hashtag:        hashtag string to search for
                    search_after:   date in YYYY-MM-DD format
                    limit:          default:None
                                    limit number of items returned
                    as_dataframe:   default:True
                                    whether to return as pandas dataframe
                    filter_retweet: default:True
                                    filter retweets from results
        outputs:    pd.DataFrame/List of tweets from search terms
        '''
        # check data types are correct
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
                
        # run search function using Cursor
        self.tweets = tw.Cursor(
            self.api.search,
            q = hashtag,
            lang="en",
            since=search_after
        ).items(10)
    
    def export(self):
        '''
        purpose:    export saved search results to a csv file in current directory
        inputs:     must have previously run search (error raise)
        outputs:    results.csv in current
        '''



if __name__ == '__main__':
    neo = MrAnderson()
    neo.search('blm','2020-06-01')
    
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import credentials
import json
import pandas as pd
import numpy as np
import sys


def get_track_data():
    df = pd.read_excel(r'location_data.xlsx')
    track = []
    for column in df:
        # Select column contents by column name using [] operator
        track += [i.lower() for i in list(df[column]) if type(i) != float]
    return track


class StdOutListener(StreamListener):

    tweet_number = 0   # class variable

    def __init__(self, fetched_tweets_filename, max_tweets):
        self.fetched_tweets_filename = fetched_tweets_filename
        self.max_tweets = max_tweets  # max number of tweets

    def on_data(self, data):
        self.tweet_number += 1
        try:
            tweet = json.loads(data)
            print(tweet)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)

        except BaseException:
            print('Error')
            pass
        if self.tweet_number >= self.max_tweets:
            sys.exit('Limit of '+str(self.max_tweets)+' tweets reached.')

    def on_error(self, status):
        print("Error " + str(status))
        if status == 420:
            print("Rate Limited")
            return False


if __name__ == '__main__':

    # This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
    auth.set_access_token(credentials.ACCESS_TOKEN,
                          credentials.ACCESS_TOKEN_SECRET)

    # data will be transported to this file
    fetched_tweets_filename = "tweets.json"
    # max number of tweets to be collected
    l = StdOutListener(fetched_tweets_filename, 50)
    stream = Stream(auth, l)
    track = get_track_data()
    stream.filter(track=track)

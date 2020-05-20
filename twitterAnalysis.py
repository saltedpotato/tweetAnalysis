import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from twitterStreamedData import get_track_data
from textblob import TextBlob
import re


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """

    def analyse_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(
            data=[tweet['text'] for tweet in tweets], columns=['tweets'])

        df['user_location'] = np.array(
            [tweet["user"]["location"] for tweet in tweets])
        df['location_posted'] = np.array(
            [tweet["place"]["full_name"] if tweet["place"] is not None else "No input" for tweet in tweets])
        df['date'] = np.array([tweet["created_at"] for tweet in tweets])
        df['likes'] = np.array([tweet["retweeted_status"]["favorite_count"]
                                if "retweeted_status" in tweet else 0 for tweet in tweets])
        df['retweets'] = np.array([tweet["retweeted_status"]["retweet_count"]
                                   if "retweeted_status" in tweet else 0 for tweet in tweets])

        return df

    def classify_data(self, track_data, tweets):
        classfied_data = {}
        for data in track_data:
            classfied_data[data] = 0

        for tweet in tweets:
            text = tweet["text"]
            for word in text:
                if word.lower() in track_data:
                    classfied_data[word] += 1
        return classfied_data


if __name__ == "__main__":
    tweets = []
    with open('tweets.json') as f:
        lines = f.read().splitlines()
    for json_obj in lines:
        if json_obj != '':
            loaded_json = json.loads(json_obj)
            tweets.append(loaded_json)

    tweet_analyzer = TweetAnalyzer()
    df = tweet_analyzer.tweets_to_data_frame(tweets)

    """
    time series
    """
    # time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    # time_likes.plot(figsize=(16, 4), label="likes", legend=True)
    # time_retweet = pd.Series(data=df['retweets'].values, index=df['date'])
    # time_retweet.plot(figsize=(16, 4), label="rewteets", legend=True)
    # plt.show()

    '''
    sentiment analysis
    '''
    df['sentiment'] = np.array([tweet_analyzer.analyse_sentiment(tweet) for tweet in df['tweets']])
    print(df.head(10))
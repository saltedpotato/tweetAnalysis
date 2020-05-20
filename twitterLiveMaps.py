from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import credentials
from pykafka import KafkaClient
import json
import sys


def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')


class StdOutListener(StreamListener):

    tweet_number = 0   # class variable

    def __init__(self, fetched_tweets_filename, max_tweets=None):
        self.fetched_tweets_filename = fetched_tweets_filename
        self.max_tweets = max_tweets  # max number of tweets

    def on_data(self, data):
        self.tweet_number += 1
        try:
            message = json.loads(data)
            print(message)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            if message['place'] is not None:
                client = get_kafka_client()
                topic = client.topics['twitterdata1']
                producer = topic.get_sync_producer()
                producer.produce(data.encode('ascii'))
            '''
            elif message['user']["location"] is not None:
                client = get_kafka_client()
                topic = client.topics['twitterdata1']
                producer = topic.get_sync_producer()
                producer.produce(data.encode('ascii'))
            '''

        except BaseException as e:
            print("Error on_data %s" % str(e))
            pass
        # if self.tweet_number >= self.max_tweets:
        #     sys.exit('Limit of '+str(self.max_tweets)+' tweets reached.')

    def on_error(self, status):
        print("Error " + str(status))
        if status == 420:
            print("Rate Limited")
            return False


if __name__ == "__main__":
    auth = OAuthHandler(credentials.API_KEY, credentials.API_SECRET_KEY)
    auth.set_access_token(credentials.ACCESS_TOKEN,
                          credentials.ACCESS_TOKEN_SECRET)

    fetched_tweets_filename = "tweets.json"
    listener = StdOutListener(fetched_tweets_filename)

    stream = Stream(auth, listener)
    stream.filter(locations=[
                  103.6920359, 1.1304753, 104.0120359, 1.4504753])

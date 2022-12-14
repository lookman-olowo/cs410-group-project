import tweepy
import re
from flask import Flask
from tweepy import OAuthHandler
from textblob import TextBlob
app = Flask(__name__)
SEARCH_CORPUS = []
class TwitterClient(object):
    def __init__(self):
        F = open('API_Keys.txt', 'r').readlines()
        consumer_key = F[0].split(":")[1].strip()
        consumer_secret = F[1].split(":")[1].strip()
        access_token = F[2].split(":")[1].strip()
        access_token_secret = F[3].split(":")[1].strip()
        bearer_token = r"AAAAAAAAAAAAAAAAAAAAAOXwjAEAAAAAzSEYMbVvuYyDEBs%2FMzrCfArRD1o%3D0GLEDRL8dClUcsUyXmkrIxLS9WsTillEnyAOFkHDymoNMqbGPf"
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
            self.client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)
        except:
            print("Error: Authentication Failed")
    def clean_tweet(self, tweet):
        """
      Utility function to clean tweet text by removing links, special characters
      using simple regex statements.
      """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    def get_tweet_sentiment(self, tweet):
        """
      Utility function to classify sentiment of passed tweet
      using textblob's sentiment method
      Return as tuple (sentiment, subjectivity)
        """
        analysis = TextBlob(self.clean_tweet(tweet))

        subjectivity = analysis.sentiment.subjectivity

        if analysis.sentiment.polarity > 0:
            return ('positive', subjectivity)
        elif analysis.sentiment.polarity == 0:
            return ('neutral', subjectivity)
        else:
            return ('negative', subjectivity)


    def get_tweets(self, query, count=10):
        """
      Main function to fetch tweets and parse them.
      """
        
        tweets = []
        try:
            # With this, I get the error: AttributeError: 'API' object has no attribute 'search'. This could be a
            # versioning issue fetched_tweets = self.api.search(q = query, count = count)
            fetched_tweets = self.api.search_tweets(q=query, count=count, tweet_mode="extended")
            instance = self.add_to_recent(query)
            recents = self.get_recent_searches()
            print("Recent searches are the following: {}".format(recents))
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['id'] = tweet.id
                parsed_tweet['text'] = tweet.full_text.split('http')[0]
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.full_text.split('http')[0])[0]
                parsed_tweet['subjectivity'] = round(self.get_tweet_sentiment(tweet.full_text.split('http')[0])[1], 2)
                parsed_tweet['source'] = tweet.user.screen_name
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        # The commented code gave me the error: AttributeError: module 'tweepy' has no attribute 'TweepError'. This
        # could be a versioning issue except tweepy.TweepError as e:
        except tweepy.errors.TweepyException as e:
            print("Error : " + str(e))
    def query_twitter_users(self, query, count, user_list=[]):
        """
        Main function to fetch tweets and parse them.
        """
        tweets = []
        try:
            # With this, I get the error: AttributeError: 'API' object has no attribute 'search'. This could be a
            # versioning issue fetched_tweets = self.api.search(q = query, count = count)
            fetched_tweets = []
            if query == None:
                for user in user_list:
                    fetched_tweets += self.api.search_tweets(q="from:{}".format(user), tweet_mode="extended")
                    # print("Fetched tweets: {}".format(fetched_tweets))
                    for tweet in fetched_tweets:
                        parsed_tweet = {}
                        parsed_tweet['id'] = tweet.id
                        parsed_tweet['text'] = tweet.full_text.split('http')[0]
                        parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.full_text.split('http')[0])[0]
                        parsed_tweet['subjectivity'] = round(self.get_tweet_sentiment(tweet.full_text.split('http')[0])[1], 2)
                        parsed_tweet['source'] = user
                        if tweet.retweet_count > 0:
                            if parsed_tweet not in tweets:
                                tweets.append(parsed_tweet)
                        else:
                            tweets.append(parsed_tweet)
                return
            else:
                for user in user_list:
                    fetched_tweets += self.api.search_tweets(q="from:{} {}".format(user, query), tweet_mode="extended")
                    # print("Fetched tweets: {}".format(fetched_tweets))
                    for tweet in fetched_tweets:
                        parsed_tweet = {}
                        parsed_tweet['text'] = tweet.full_text.split('http')[0]
                        parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.full_text.split('http')[0])[0]
                        parsed_tweet['subjectivity'] = round(self.get_tweet_sentiment(tweet.full_text.split('http')[0])[1], 2)
                        parsed_tweet['source'] = user
                        if tweet.retweet_count > 0:
                            if parsed_tweet not in tweets:
                                tweets.append(parsed_tweet)
                        else:
                            tweets.append(parsed_tweet)
            return tweets
        # The commented code gave me the error: AttributeError: module 'tweepy' has no attribute 'TweepError'. This
        # could be a versioning issue except tweepy.TweepError as e:
        except tweepy.errors.TweepyException as e:
            print("Error : " + str(e))
    def add_to_recent(self, query):
        if len(SEARCH_CORPUS) >= 9: 
            SEARCH_CORPUS.pop(0)
        SEARCH_CORPUS.append(query.lower())
    
    def get_recent_searches(self):
        return SEARCH_CORPUS


def search():
    query = input("What would you like to search on Twitter?\n")
    return query

def main(_query):
    api = TwitterClient()
    query_ = _query
    #   When count = 200, I get the error: Max retries exceeded with url: /1.1/search/tweets.json
    #   tweets = api.get_tweets(query = query_, count = 200)
    tweets = api.get_tweets(query=query_, count=50)
    
    positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("Positive tweets percentage: {} %".format(100 * len(positive_tweets) / len(tweets)))
    negative_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {} %".format(100 * len(negative_tweets) / len(tweets)))
    print("Neutral tweets percentage: {} % \
      ".format(100 * (len(tweets) - (len(negative_tweets) + len(positive_tweets))) / len(tweets)))
    print("\n\nPositive tweets:")
    for tweet in positive_tweets[:10]:
        print(tweet['text'])
    print("\n\nNegative tweets:")
    for tweet in negative_tweets[:10]:
        print(tweet['text'])

if __name__ == "__main__":
    main()

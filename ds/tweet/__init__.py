from typing import List, Tuple

import tweepy
import json
from textblob import TextBlob


def run_search(search: str, location: Tuple[float, float]):
    twitter_config = 'twitter.json'
    with open(twitter_config) as f:
        config = json.loads(f.read())
    auth = tweepy.OAuthHandler(**config['consumer_token'])
    auth.set_access_token(**config['access_token'])
    tapi = tweepy.API(auth)
    long, lat = location
    places = tapi.geo_search(long=long, lat=lat, granularity='city')
    return tapi.search(f"{search} -place:{places[0].id} -filter:retweets", include_entities=False, )



def analyse_sentiment(tweets):
    # for tweet in tweets:
    #     print(f"TWEET: {tweet.text}")
    #     b = TextBlob(tweet.text)
    #     print(f"ANALYSIS: {b.sentiment} {b.tags} {b.sentiment_assessments}")
    return [(TextBlob(t.text), t) for t in tweets]
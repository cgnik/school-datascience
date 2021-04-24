from argparse import ArgumentParser
from typing import List

import tweepy
import json
from textblob import TextBlob


def run_search(search_terms: List[str], include_retweet=False):
    twitter_config = 'twitter.json'
    with open(twitter_config) as f:
        config = json.loads(f.read())
    auth = tweepy.OAuthHandler(**config['consumer_token'])
    auth.set_access_token(**config['access_token'])
    tapi = tweepy.API(auth)
    places = tapi.geo_search(query="USA", granularity="country")
    search = ' OR '.join([f"({s})" for s in search_terms])
    search = f"{search} -place:{places[0].id} {'' if include_retweet else '-filter:retweets'}"
    return tapi.search(search, include_entities=False)


def analyse_sentiment(tweets):
    for tweet in tweets:
        print(f"TWEET: {tweet.text}")
        b = TextBlob(tweet.text)
        print(f"ANALYSIS: {b.sentiment} {b.tags} {b.sentiment_assessments}")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('search', type=str, nargs='+', metavar='N')
    args = parser.parse_args()
    results = run_search(args.search)
    analyse_sentiment(results)

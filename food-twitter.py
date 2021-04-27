import bz2
import json
import os
from enum import Enum, auto

import numpy as np
import pandas as pd
import multiprocessing as mp

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style('darkgrid')


class FailType(Enum):
    PLACE = auto()
    COORD = auto()
    TEXT = auto()
    COUNTRY = auto()
    LANG = auto()


# coordinates can apparently happen in any of the following, according to
# jq -c 'paths | select(.[-1] == "coordinates")' test.json | sort | uniq
# ["coordinates"]
# ["coordinates","coordinates"]
# ["geo","coordinates"]
# ["place","bounding_box","coordinates"]
def filter_tweets(t):
    fails = {}

    def fail(t: FailType):
        fails[t] = fails.get(t, 0) + 1

    # subset the tweets looking for specific terms
    filter_terms = frozenset(('food', 'eat', 'grocery', 'market', 'supermarket', 'travel', 'far', 'miles'))
    filter_count = len(filter_terms)
    filter_min = filter_count - 2  # have to match at least 2 words

    if t is None:
        return False
    # only care if it's in the US, or at least in english
    if t.get('lang') != 'en':
        return False
    place = t.get('place') or {}
    if not place or place.get('country_code') != 'US':
        #     fail(FailType.COUNTRY)
        return False
    # only care if we can place it
    box = place.get('bounding_box')
    if not box or not box.get('coordinates'):
        fail(FailType.COORD)
        return False
    text = t.get('text').lower()
    # only care if it mentions at least 2 of the keywords
    if len(filter_terms.difference(set(text.split()))) > filter_min:
        fail(FailType.TEXT)
        return False
    return True


def tweet_files(percent: float):
    # DEFERRING: not going to pull the tweets - found an archive and i'll use that
    # tweets = run_search(['grocery', 'food', 'far', 'enough', 'hunger', 'hungry'])
    with open('data/tweets/files.txt') as f:
        all_files = [l.strip().replace('./', 'data/tweets/') for l in f.readlines()]
    if percent >= 1:
        return all_files
    print(f"Found total of {len(all_files)} twitter files")
    files = list({all_files[i] for i in np.random.randint(0, len(all_files), int(percent * len(all_files)))})
    print(f"Selected {len(files)} twitter files")
    return files


def file_gen(file_list):
    for f in file_list:
        yield f
    return


MIN_TWEET_LEN = 10000


def file_gen_tweets(file_list, tweets):
    used = []
    while len(tweets) < MIN_TWEET_LEN and len(used) < len(file_list):
        f = file_list[np.random.randint(0, len(file_list), 1)[0]]
        while f in used and len(used) < len(file_list):
            f = file_list[np.random.randint(0, len(file_list), 1)[0]]
        used.append(f)
        yield f
    if len(used) == len(file_list):
        print(f"Used all of the file list")
    return


def scan_file(file_name):
    tweets = []
    with bz2.open(file_name, 'rt', encoding="utf-8", newline='\r\n') as f:
        for line in f.readlines():
            t = json.loads(line)
            if not t:
                raise IOError(f"Unable to translate '{line}' into json")
            if filter_tweets(t):
                tweets.append(t)
    return tweets


def comb_tweets(out_file: str):
    tweets = []

    files = tweet_files(1.0)

    with mp.Pool(mp.cpu_count() - 2) as pool:
        # for i, file_name in enumerate(files):
        count = len(files)
        finished = 0
        for response in pool.imap(scan_file, file_gen_tweets(files, tweets)):
            finished += 1
            if isinstance(response, Exception):
                print(f"ERROR ERROR {response}")
            else:
                tweets += response
                print(
                    f"\r{finished}/{len(files)} ({int(100 * finished / len(files))}%) files consumed; found {len(tweets)} tweets...",
                    end='')
    print(f"Discovered {len(tweets)} tweets to scrape; writing to {out_file}")
    with open(out_file, 'wt') as st:
        for tw in tweets:
            st.write(json.dumps(tw))
            st.write('\n')
    return out_file


def search_tweets(out_file: str):
    from ds.tweet.__main__ import run_search
    run_search()


if __name__ == '__main__':
    saved_tweets = f"data/output/saved_tweets.txt"
    if not os.path.exists(saved_tweets):
        # comb_tweets(saved_tweets)
        search_tweets(saved_tweets)
    with open(saved_tweets) as st:
        tweets = [json.loads(s) for s in st.readlines()]

    applicable = list(filter(filter_tweets, tweets))
    sentiments = [(TextBlob(t.get('text')), t) for t in applicable]


    def detweet(sentiment, tweet):
        coord = tweet.get('place').get('bounding_box').get('coordinates')
        a = np.array(coord).mean(axis=1)[0]
        long, lat = a[0], a[1]
        return [tweet.get('text'), long, lat, sentiment.subjectivity, sentiment.polarity]


    td = pd.DataFrame([detweet(s, t) for s, t in sentiments],
                      columns=['text', 'longitude', 'latitude', 'subjectivity', 'polarity'])

    from shapely.geometry import Point
    import geopandas as gpd
    from geopandas import GeoDataFrame

    plotz = td[['longitude', 'latitude']]
    geometry = [Point(xy) for xy in zip(td.longitude, td.latitude)]
    gdf = GeoDataFrame(plotz, geometry=geometry)

    # this is a simple map that goes with geopandas
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))
    dink = gdf.plot(ax=world.plot(figsize=(10, 6)), marker='o', color='red', markersize=15)
    # gdf.show()
    # https://towardsdatascience.com/visualizing-tweet-vectors-using-python-e528358bce68
    # vectorizer = TfidfVectorizer(decode_error='replace', strip_accents='unicode',
    #                              stop_words='english')
    # X = vectorizer.fit_transform(td.text)
    # y = []

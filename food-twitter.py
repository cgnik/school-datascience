import bz2
import json
from enum import Enum, auto

import numpy as np
import pandas as pd
import multiprocessing as mp

from textblob import TextBlob
import seaborn as sns
import matplotlib as plt

sns.set_style('darkgrid')


class FailType(Enum):
    PLACE = auto()
    COORD = auto()
    TEXT = auto()
    COUNTRY = auto()


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
    filter_terms = frozenset(('food', 'eat', 'grocery', 'market', 'supermarket', 'travel', 'far', 'miles', ''))
    filter_count = len(filter_terms)
    filter_min = filter_count - 2  # have to match at least 2 words

    if t is None:
        return False
    # only care if it's in the US
    place = t.get('place') or {}
    # if not place or place.get('country_code') != 'US':
    #     fail(FailType.COUNTRY)
    #     return False
    # only care if we can place it
    box = place.get('bounding_box')
    if not box or not box.get('coordinates'):
        fail(FailType.COORD)
        return False
    text = t.get('text').lower()
    # only care if it mentions at least 2 of the keywords
    if len(filter_terms.difference(set(text.split()))) > filter_min:
        fail(FailType.TEXT)
        return False, FailType.TEXT
    return True


def tweet_files(percent: float):
    # DEFERRING: not going to pull the tweets - found an archive and i'll use that
    # tweets = run_search(['grocery', 'food', 'far', 'enough', 'hunger', 'hungry'])
    with open('data/tweets/files.txt') as f:
        all_files = [l.strip().replace('./', 'data/tweets/') for l in f.readlines()]
    print(f"Found total of {len(all_files)} twitter files")
    files = list({all_files[i] for i in np.random.randint(0, len(all_files), int(percent * len(all_files)))})
    print(f"Selected {len(files)} twitter files")
    return files


def file_gen(file_list):
    for f in file_list:
        yield f
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


if __name__ == '__main__':
    tweets = []

    files = tweet_files(0.20)

    with mp.Pool(mp.cpu_count() - 2) as pool:
        # for i, file_name in enumerate(files):
        count = len(files)
        finished = 0
        for response in pool.imap(scan_file, file_gen(files)):
            finished += 1
            if isinstance(response, Exception):
                print(f"ERROR ERROR {response}")
            else:
                tweets += response
                print(f"\r{finished}/{len(files)}: {int(100 * finished / len(files))}% complete...", end='')
    # print(f"\nFailures: {fails}\nGathered {len(tweets)} matching tweets\nEXAMPLE: {tweets[0] if len(tweets) > 0 else 'None'}")
    # %%
    print(f"Discovered {len(tweets)} tweets to scrape")

    applicable = list(filter(filter_tweets, tweets))
    sentiments = [(TextBlob(t.get('text')), t) for t in applicable]


    def detweet(sentiment, tweet):
        lat = long = 0
        ll = np.array(tweet.get('place').get('coordinates'))
        return [tweet.get('text'), lat, long, sentiment.subjectivity, sentiment.polarity]


    pd.DataFrame([detweet(s, t) for s, t in sentiments], columns=['text', 'lat', 'long', 'subjectivity', 'polarity'])

    plt.plot()

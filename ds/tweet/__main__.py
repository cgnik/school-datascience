from argparse import ArgumentParser

from ds.tweet import run_search, analyse_sentiment

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('search', type=str, nargs='+', metavar='N')
    args = parser.parse_args()
    results = run_search(args.search)
    analyse_sentiment(results)

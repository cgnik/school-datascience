from argparse import ArgumentParser

from ds.tweet import run_search, analyse_sentiment

if __name__ == '__main__':
    # parser = ArgumentParser()
    # parser.add_argument('search', type=str, nargs='+', metavar='N')
    # args = parser.parse_args()
    search = "groceries AND store AND far"
    results = run_search(search, location=(-74.0360765, 40.7445621))
    print(results)
    analyse_sentiment(results)

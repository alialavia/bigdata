from argparse import ArgumentParser
from twitternews.processing import featurize
from twitternews.io import iterate_tweets
from twitternews.util import keep_progress


def main():
    """
    Entry point of the application
    """
    parser = ArgumentParser()
    parser.add_argument('-d', '--twitter_directory', dest='twitter_directory', type=str, required=True,
                        metavar='/path/to/twitter/files', help='The directory where twitter data files can be found')
    arguments = parser.parse_args()

    for tweet in keep_progress(iterate_tweets(arguments.twitter_directory)):
        vector = featurize(tweet['text'])


if __name__ == "__main__":
    main()

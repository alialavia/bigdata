from requests_oauthlib import OAuth1
from time import sleep, strftime
import requests
import logging
import sys, getopt

TIMEOUT = 60
MAX_TWEETS_IN_FILE = 100000
APP_KEY = "OuooZ8GbWmuWEw6j6Dw61d9Mz"
APP_SECRET = "BAtyvHU74Hx28XQniFadSaZw1wKvjkUK29AxxFyb9SzQnqA4bh"
OAUTH_TOKEN = "34725972-00fHS1H3rbWX6HEQT1M6beDlAFZuCheJn5GIlXv54"
OAUTH_TOKEN_SECRET = "Dbj1GG8bIFYoAoizgEfRKd1zLLtn0qq95E4mStNfYNDSy"


class TwitterStream(object):
    def __init__(self, consumer_key=None, consumer_secret=None, access_token_key=None, access_token_secret=None):
        self.auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)

    def request_tweets(self, params=None):
        session = requests.Session()
        session.auth = self.auth
        session.stream = True
        timeout = 90 # Twitter recommendation for streaming API
        url = "https://stream.twitter.com/1.1/statuses/filter.json"
        self.response = session.request("POST", url, data=params, params=params, timeout=timeout)

    def __iter__(self):
        for item in self.response.iter_lines(chunk_size=512):
            if item:
                yield item


def get_new_filename(basename=""):
    return "%s%s" % (basename, strftime("%Y%m%d%H%M%S"))


def main(argv):
    e = 1
    helpstring = "usage: twitter.py {-e [E]}"
    logger = logging.getLogger("twitter")
    loghandler = logging.FileHandler("twitter.log")
    loghandler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(loghandler)
    logger.setLevel(logging.INFO)

    twitter_stream = TwitterStream(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    try:
        opts, args = getopt.getopt(argv, "he:", ["every="])
    except getopt.GetoptError:
        print helpstring
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print helpstring
            sys.exit()
        elif opt in ("-e", "--every"):
            try:
                e = int(arg)
                if e<1:
                    print "e should be set a positive non-zero number"
                    sys.exit()
            except ValueError:
                print "e should be set a positive non-zero number"
                sys.exit()



    while True:
        output_stream = None
        try:

            twitter_stream.request_tweets({'locations':'-180,-90,180,90', 'language':'en'})
            logger.info("Requested twitter stream")
            logger.info("Saving every " + `e` + " tweets")

            tweet_count = 0
            output_stream = file(get_new_filename("twitter-"), "w")
            logger.info("Opened output file %s" % output_stream.name)

            logger.info("Writing results")
            for item in twitter_stream:

                if tweet_count % e == 0:
                    output_stream.write(item)
                    output_stream.write("\n")

                tweet_count += 1

                # If we reach the maximum number of tweets, we move to a new file
                if tweet_count >= MAX_TWEETS_IN_FILE:
                    output_stream.close()
                    output_stream = file(get_new_filename("twitter-"), "w")
                    logger.info("Opened next file: %s" % output_stream.name)
                    tweet_count = 0

        except Exception as e:
            logger.error(e.message)

        finally:
            if output_stream is not None and not output_stream.closed:
                output_stream.close()
            logger.info("Retrying connection in %d seconds" % TIMEOUT)
            sleep(TIMEOUT)


if __name__ == "__main__":
    main(sys.argv[1:])


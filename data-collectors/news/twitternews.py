from requests_oauthlib import OAuth1
from time import sleep, strftime
import requests
import logging
import json
from StringIO import StringIO

CONFIG_FILE = "twitternews.config"

APP_KEY = "OuooZ8GbWmuWEw6j6Dw61d9Mz"
APP_SECRET = "BAtyvHU74Hx28XQniFadSaZw1wKvjkUK29AxxFyb9SzQnqA4bh"
OAUTH_TOKEN = "34725972-00fHS1H3rbWX6HEQT1M6beDlAFZuCheJn5GIlXv54"
OAUTH_TOKEN_SECRET = "Dbj1GG8bIFYoAoizgEfRKd1zLLtn0qq95E4mStNfYNDSy"

TIMEOUT = 10
REQUEST_DELAY = 5
class TwitterNews(object):
    def __init__(self, consumer_key=None, consumer_secret=None, access_token_key=None, access_token_secret=None):
        self.auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)

    def request_tweets(self, params=None):                
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        self.response = requests.get(url, params=params, auth=self.auth, timeout=TIMEOUT)


def get_newssources():
    screen_names=[]
    file_names=[]
    
    try:
        config_file = open(CONFIG_FILE,"r")
        for line in config_file:
            if line[0]=="#":
                continue
            if screen_names==[]:
                screen_names = map(trim, line.split(','))
            elif file_names==[]:
                file_names = map(trim, line.split(','))
            else:
                print "Error: config file cannot have more than two uncommented lines"
                return None   
    except Exception as e:
        print e.message
        return None

    return zip(screen_names, file_names)

def trim (s) : return s.strip()
def main():
    logger = logging.getLogger("twitternews")
    loghandler = logging.FileHandler("twitternews.log")
    loghandler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(loghandler)
    logger.setLevel(logging.INFO)

    twitter_news = TwitterNews(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    

    
    
    news_sources = get_newssources();
    #initialize last tweet id
    last_id = {}
    for elem in news_sources:
        last_id[elem[0]] = 1
    
    while True:
        output_stream = None
        try:    
            for elem in news_sources:
                screen_name = elem[0]
                file_name = elem[1]
                
                logger.info ("Requesting from @%s and write to %s" % (screen_name, file_name))
                twitter_news.request_tweets({'screen_name':screen_name, 'exclude_replies':'true', 'count':'1000', 'since_id' : last_id[screen_name]})                    
                posts = json.load(StringIO(twitter_news.response.content))            

                if twitter_news.response.status_code!=200:   #if there is any error with the response, log it and try next news_source
                    logger.error( "Error Code: %d, %s" % (twitter_news.response.status_code, twitter_news.response.content))         
                    continue

                output_stream = file(file_name, "a+")
                logger.info("Opened output file %s" % output_stream.name)
                
                logger.info("Writing %d results from %s\n\n" % (len(posts), screen_name) )                
                for item in posts:                                        
                    extract_news = json.dumps({"headlines": item['text'], "date": item['created_at'], "abstract": item['text'], "keywords": item['text'], "source": screen_name}, 
                        sort_keys=True)
                    output_stream.write(json.dumps(item))
                    output_stream.write("\n")
                    id = item['id']
                    last_id[screen_name] = max(last_id[screen_name], id) 

                sleep(REQUEST_DELAY) # a delay to keep with tweeter request frequency requirements

        except Exception as e:
            logger.error(e.message)

        finally:
            if output_stream is not None and not output_stream.closed:
                output_stream.close()    
            


if __name__ == "__main__":
    main()


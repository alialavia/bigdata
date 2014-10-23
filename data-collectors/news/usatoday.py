from time import sleep, strftime
import requests
import logging
import json

TIMEOUT = 60*60*24 #wait for a full day
PAGE_OFFSET = 20
API_KEY = "jf2nyj9uvxnjfq2u8ebzyhjm"
API_URL = "http://api.usatoday.com/open/articles/topnews/home"

def getNews():
  logger = logging.getLogger("usatoday")
  loghandler = logging.FileHandler("usatoday.log")
  loghandler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
  logger.addHandler(loghandler)
  logger.setLevel(logging.INFO)
  
  while True: 
    output_stream = None
    try:
      url_param = {'api_key':API_KEY, 'encoding':'json', 'count':'1000', 'days':'1'}
      news = requests.get(API_URL, params=url_param)
      if (news.status_code == 200):
        print(news.url)
        output_stream = file(get_new_filename("usatoday-"), "w")
        logger.info("Opened output file %s" % output_stream.name)
        print news.text
        output_stream.write(news.text)
      elif (news.status_code == 500):
        raise Exception("internal server error")
    except Exception as e:
      logger.error(e.message) 
      sleep(TIMEOUT)
      continue
    finally:
      if output_stream is not None and not output_stream.closed:
        output_stream.close()
      logger.info("")

def get_new_filename(basename=""):
  return "%s%s" % (basename, strftime("%Y%m%d%H%M%S"))

def main():
  getNews()


if __name__ == "__main__":
  main()


from time import sleep, strftime
import requests
import logging
import json

TIMEOUT = 60
PAGE_OFFSET = 20
API_KEY = "7ab9f172013a49a87d5e915a496c4468:17:69854008"
API_URL = "http://api.nytimes.com/svc/news/v3/content/all/all.json"

def getNewsWireCount():
  url_param = {'api-key':API_KEY, 'offset':'1'}
  news = requests.get(API_URL, params=url_param)
  jnews = json.loads(news.text)
  return jnews["num_results"]

def getNewsWire(total_cnt):
  logger = logging.getLogger("nyt")
  loghandler = logging.FileHandler("nyt.log")
  loghandler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
  logger.addHandler(loghandler)
  logger.setLevel(logging.INFO)
  offset = 1
  
  while offset < total_cnt: 
    try:
      url_param = {'api-key':API_KEY, 'offset':offset}
      news = requests.get(API_URL, params=url_param)
      print(news.url)
      offset = offset + 20
      output_stream = file(get_new_filename("nyt-"), "w")
      logger.info("Opened output file %s" % output_stream.name)
      output_stream.write(news.text)
    except Exception as e:
       print(e) 
    finally:
      output_stream.close()

def get_new_filename(basename=""):
  return "%s%s" % (basename, strftime("%Y%m%d%H%M%S"))

def main():
  total_cnt = getNewsWireCount()
  getNewsWire(total_cnt)


if __name__ == "__main__":
  main()


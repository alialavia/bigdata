import os
import json
from urlparse import urlparse
from time import sleep, strftime

DATA_PATH = 'nyt_data/'

def main():
  news_count = 0
  output_stream = file(get_new_filename("news-model-technology-"), "w")
  for filename in os.listdir(DATA_PATH):
    print filename
    f = open(DATA_PATH + filename, 'r')
    try:
      newsArray = json.loads(f.readline())
      for news in newsArray['results']:
        if (news['section'] and news['section'] == "Technology"):
          if news['title']:         title      = news['title'] 
          if news['published_date']:date       = news['published_date'] 
          if news['abstract']:      abstract   = news['abstract'] 
          if news['url']:           url_keywords = urlparse(news['url']).path.split('/')[4]
          if news['source']:        source     = news['source'] 
          output_stream.write(json.dumps({"title": title, "date": date, "abstract": abstract, "url_keywords": url_keywords, "source": source}, sort_keys=True))
          output_stream.write("\n")
          news_count += 1
          print news_count

    except (ValueError, KeyError, TypeError, IndexError):
      print "JSON Format error"
      continue

def get_new_filename(basename=""):
  return "%s%s" % (basename, strftime("%Y%m%d%H%M%S"))

if __name__ == "__main__":
  main()

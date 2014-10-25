import os
import json
from urlparse import urlparse
from time import sleep, strftime

DATA_PATH = 'usatoday_data/'

def main():
  tech_output_stream     = file(get_new_filename("news-model-usatoday-"), "w")
  for filename in os.listdir(DATA_PATH):
    print filename
    f = open(DATA_PATH + filename, 'r')
    try:
      newsArray = json.loads(f.readline())
      for news in newsArray['stories']:
        '''
        extract data for news data model:
        1. Headlines
        2. Keywords: extract if exists, otherwise extract from url
        3. Date
        4. Summary/Description/Abstract/Snippet
        5. News source
        '''
        print news
        if news['title']:         headlines  = news['title'] 
        if news['pubDate']:       date       = news['pubDate'] 
        if news['description']:   abstract   = news['description'] 
        if news['link']:          keywords = urlparse(news['link']).path.split('/')[8]
        source     = 'usatoday' 
        tech_output_stream.write(json.dumps({"headlines": headlines, "date": date, "abstract": abstract, "keywords": keywords, "source": source}, sort_keys=True))
        tech_output_stream.write("\n")

    except (ValueError, KeyError, TypeError, IndexError):
      print "JSON Format error"
      continue

def get_new_filename(basename=""):
  return "%s%s" % (basename, strftime("%Y%m%d%H%M%S"))

if __name__ == "__main__":
  main()

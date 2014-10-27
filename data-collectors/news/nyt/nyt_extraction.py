import os
import json
from urlparse import urlparse
from time import sleep, strftime

DATA_PATH = 'nyt_data/'

def main():
  tech_output_stream     = file(get_new_filename("news-model-technology-"), "w")
  sport_output_stream    = file(get_new_filename("news-model-sports-"), "w")
  politics_output_stream = file(get_new_filename("news-model-politics-"), "w")
  for filename in os.listdir(DATA_PATH):
    print filename
    f = open(DATA_PATH + filename, 'r')
    try:
      newsArray = json.loads(f.readline())
      for news in newsArray['results']:
        '''
        extract data for news data model:
        1. Headlines
        2. Keywords: extract if exists, otherwise extract from url
        3. Date
        4. Summary/Description/Abstract/Snippet
        5. News source
        '''
        if news['title']:         headlines  = news['title'] 
        if news['published_date']:date       = news['published_date'] 
        if news['abstract']:      abstract   = news['abstract'] 
        if news['source']:        source     = news['source'] 
 
        if (news['section'] and news['section'] == "Technology"):
          if urlparse(news['url']).netloc.find("blog") == -1:
            if news['url']:           keywords = urlparse(news['url']).path.split('/')[5]
          else:
            if news['url']:           keywords = urlparse(news['url']).path.split('/')[4]
          tech_output_stream.write(json.dumps({"headlines": headlines, "date": date, "abstract": abstract, "keywords": keywords, "source": source}, sort_keys=True))
          tech_output_stream.write("\n")
          print "Technology"
        elif (news['section'] and news['section'] == "Sports"):
          if news['url']:           keywords = urlparse(news['url']).path.split('/')[5]
          sport_output_stream.write(json.dumps({"headlines": headlines, "date": date, "abstract": abstract, "keywords": keywords, "source": source}, sort_keys=True))
          sport_output_stream.write("\n")
          print "Sports"
        elif (news['section'] and news['section'] == "politics"):
          if news['url']:           keywords = urlparse(news['url']).path.split('/')[5]
          politics_output_stream.write(json.dumps({"headlines": headlines, "date": date, "abstract": abstract, "keywords": keywords, "source": source}, sort_keys=True))
          politics_output_stream.write("\n")
          print "Politics"

    except (ValueError, KeyError, TypeError, IndexError):
      print "JSON Format error"
      continue

def get_new_filename(basename=""):
  return "%s%s" % (basename, strftime("%Y%m%d%H%M%S"))

if __name__ == "__main__":
  main()

"""
Read a twitter classified file into a dictionary and write it to the stdout
"""

from nltk import pos_tag
from nltk import word_tokenize
import sys
from sys import stderr
import codecs


from time import strptime
from datetime import datetime
YEAR = 2014
if len(sys.argv) != 2:
    print "Please provide an input file with the classified tweets."
    sys.exit(0)
CAT = "politics"
fname = sys.argv[1]
#lines = [line for line in open(fname)]
twfile = codecs.open(fname, encoding='utf-8')
wordfreq = dict()
l=0
for line in twfile:
    stderr.write("\033[2K\r")
    stderr.write(str(l))
    stderr.write(" lines processed")
    l = l+1
    splitted = line.split('::')      
    if len(splitted) == 3:
        sdate = splitted[1].strip()
        category = splitted[0].strip()
        text =  splitted[2].strip().lower()
        #print "'%s' '%s' '%s' '%s'" % (sdate, category, CAT, (CAT==category))
        if category == CAT:
            tokens = pos_tag(word_tokenize(text))
            nouns = [token[0] for token in tokens if token[1].startswith('NN')]
            ddate = strptime(str(sdate), '%a %b %d %H:%M:%S')
            correctdate = datetime(YEAR, ddate.tm_mon, ddate.tm_mday, ddate.tm_hour, ddate.tm_min)        
            strdate = correctdate.strftime('%Y-%m-%d %H:%M:%S')
            for noun in nouns:
                if noun in wordfreq:
                    wordfreq[noun] += [strdate]
                else:
                    wordfreq[noun] = [strdate]

print wordfreq

# for token in pos_tag(text):
#     if token[1] == 'NN':
#         print token

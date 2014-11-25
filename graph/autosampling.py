""" Sample a sorted classfied twitter file """
import sys
from sys import stderr
import ast
import codecs
import datetime, math
from datetime import datetime
from nltk import pos_tag
from nltk import word_tokenize

import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter

# Constants

YEAR = 2014
DFMT = '%Y-%m-%d %H:%M:%S'
CAT = 'politics'
def datetoindex(startdate, currentdate, samplingfreq):
    """ Convert a date to an index based on the frequency """
    return int(math.ceil((currentdate - startdate).total_seconds() / samplingfreq))

def linetodata(line):
    """ Convert a line to a well-formed tupple """
    splitted = line.split('::')  
    # Convert the date
    date = datetime.strptime(splitted[1].strip(), '%a %b %d %H:%M:%S')
    correctdate = date.replace(year=YEAR)
    
    category = splitted[0].strip().encode('ascii','ignore')
    text = splitted[2].strip().lower().encode('ascii','ignore')
    
    return (correctdate, category, text)



fname = sys.argv[1]
startdate = datetime.strptime(sys.argv[2], DFMT)
samplingfreq = int(sys.argv[3])


#lines = [line for line in open(fname)]
twfile = codecs.open(fname, encoding='utf-8')

#print linetodata(line)

#print "File opened successfully"

timeseries = list()
startdate = datetime.strptime('2014-10-09 13:00:00',DFMT)
l=0
for line in twfile:
    stderr.write("\033[2K\r")
    stderr.write(str(l))
    stderr.write(" lines processed")
    l = l+1
    datatuple = linetodata(line)
    (date, category, text) = datatuple    
    # Only process a specific category
    timeindex = datetoindex(startdate, date, samplingfreq)
    if len(timeseries) < timeindex:
        wordfreq = dict()
        timeseries += [wordfreq]

    if category == CAT:
        tokens = pos_tag(word_tokenize(text))
        nouns = [token[0] for token in tokens if token[1].startswith('NN')]   
    
        for noun in nouns:
            if noun in wordfreq:
                wordfreq[noun] += 1
            else:
                wordfreq[noun] = 1

print timeseries

# Sample the word dictionary
import sys
import ast
import codecs
import datetime, math
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter

def datetoindex(startdate, currentdate, samplingfreq):
    return int(math.ceil((currentdate - startdate).total_seconds() / samplingfreq))

DFMT = '%Y-%m-%d %H:%M:%S'
fname = sys.argv[1]
startdate = datetime.strptime(sys.argv[2],DFMT)
enddate = datetime.strptime(sys.argv[3], DFMT)
samplingfreq = int(sys.argv[4])


#lines = [line for line in open(fname)]
twfile = codecs.open(fname, encoding='utf-8')
wordfreq = ast.literal_eval(twfile.read())

#print "File opened successfully"
timelen = datetoindex(startdate, enddate, samplingfreq)
timeseries = dict()
sys.stderr.write(str(timelen))

for word in wordfreq:
    timeseries[word] = [0] * timelen
    for datekey in wordfreq[word]:
        timestamp = datetime.strptime(datekey, DFMT)
        secdiff = datetoindex(startdate, timestamp, samplingfreq)
        
        if secdiff < 0:
            sys.stderr.write("Error. There are dates earlier than the provided start date. Please use an earlier date")
            exit(-1)
        try:
            timeseries[word][secdiff] += 1
        except:
            sys.stderr.write(str(secdiff))

print timeseries



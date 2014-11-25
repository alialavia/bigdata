import datetime
import codecs
import sys, ast
import pdb

import plotly.plotly as py
from plotly.graph_objs import *

def selecttop(d, top):
    sizes = {k : (sum(d[k]) / len(d[k])) for k in d}
    sorted(sizes, key=sizes.get)

py.sign_in("alialavia", "dlrlks5tzd")

DFMT = '%Y-%m-%d %H:%M:%S'
MINOCCURANCE = 100

#list of useless words!
FILTEROUT = ['http', 'rt', '@', 'https']
#pdb.set_trace() #BREAKPOINT

# Read parameters from command line
fname = sys.argv[1]
startdate = datetime.datetime.strptime(sys.argv[2], DFMT)
samplingfreq = int(sys.argv[3])
plotname = sys.argv[4]
# Open and load the fiel into a list
twfile = codecs.open(fname, encoding='utf-8')
timeseries = ast.literal_eval(twfile.read())
print "File was read successfully."
timestamps = len(timeseries)

# Convert the files into time series
times = [None] * timestamps
scatterdata = dict()

for i in range(len(times)):
    times[i] = startdate + datetime.timedelta(seconds=samplingfreq*i)    

for t in range(timestamps):
    for k in timeseries[t]:
        if not (k in scatterdata):
            scatterdata[k] = [0] * timestamps 
        scatterdata[k][t] = timeseries[t][k]

# filter the data. Only plot the most frquent words
filtered_data = dict()
for k in scatterdata:
    # filter some noise nouns
    if k in FILTEROUT:
        continue
    if sum(scatterdata[k]) > MINOCCURANCE:
        filtered_data[k] = scatterdata[k]

print "Coversion to time series finished successfully."
print "Number of ticks: ", timestamps
print "Number of unique nouns: ", len(scatterdata)
print "Number of filtered nouns: ", len(filtered_data)
if len(filtered_data) == 0:
    print "Filtering conditins are too tight. Consider changing MINOCCURANCE or FILTEROUT list"

#print "Length of data: ", len(dates)
print "Plotting..."
#exit(0)
#df = pd.DataFrame(scatterdata, index=dates, columns=[k for k in scatterdata])
#plt.figure(); df.plot(); plt.legend(loc='best')
#dates = pd.date_range('09-10-2014 13:00:00',periods=timestamps, freq='S')        



#fig, ax = plt.subplots()

# print len(times), len(timeseries['obama'])
data = Data([Scatter(x=times, y=filtered_data[topic],name = topic) for topic in filtered_data])

plot_url = py.plot(data, filename=plotname)

"""
ax.plot_date(times, timeseries['obama'],'-')
ax.plot_date(times, timeseries['obamacare'],'r-')

ax.fmt_xdata = DateFormatter(DFMT)
ax.autoscale_view()
fig.autofmt_xdate()
plt.show()

"""

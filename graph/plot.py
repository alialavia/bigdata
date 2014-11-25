import datetime
import codecs
import sys, ast
import pdb

import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter

import plotly.plotly as py
from plotly.graph_objs import *
py.sign_in("alialavia", "dlrlks5tzd")


DFMT = '%Y-%m-%d %H:%M:%S'
#pdb.set_trace() #BREAKPOINT
# Read parameters from command line
fname = sys.argv[1]
startdate = datetime.datetime.strptime(sys.argv[2], DFMT)
samplingfreq = int(sys.argv[3])

# Open and load the fiel into a list
twfile = codecs.open(fname, encoding='utf-8')
timeseries = ast.literal_eval(twfile.read())
print "File was read successfully."

# Convert the files into time series
times = [None] * len(timeseries.itervalues().next())
for i in range(len(times)):
    times[i] = startdate + datetime.timedelta(seconds=samplingfreq*i)
print "Coversion to time series finished successfully."

fig, ax = plt.subplots()

# print len(times), len(timeseries['obama'])

data = Data([Scatter(x=times, y=timeseries[topic],name = topic) for topic in timeseries])

plot_url = py.plot(data, filename='python-datetime')

"""
ax.plot_date(times, timeseries['obama'],'-')
ax.plot_date(times, timeseries['obamacare'],'r-')

ax.fmt_xdata = DateFormatter(DFMT)
ax.autoscale_view()
fig.autofmt_xdate()
plt.show()

"""

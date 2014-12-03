1) cat a set of twitter files into one single file. Let's call it twitts.txt
2) convert it to a time series file:
    ./totimeseries.py twitts.txt 60 politics > twitts.ts
where sampling frequency is 60 seconds and category is politics

2) Find the top 10 topics per hour (every 60 minutes) :
    ./timeanalysis.py twitts.ts 10 60

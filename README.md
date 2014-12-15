Automatic News Generation Based on Twitter
=======

The authors were motivated by a simple question: can we generate more accurate and less biased news using twitter data in comparison to traditional news agencies? Would such a system have a potential of becoming an alternative to mainstream news sources? If so, such a system could be a more reliable source of unbiased news, which in turn will have immense effect on public awareness, knowledge and discourse.

Three components are included in this system:
* Data collector
* Twitter news classifier
* Visualization of news key-terms over time

### Data Collector
In order to run the `data-collectors` scritp to collect twitter data from [Twitter Streams](https://dev.twitter.com/streaming/public), you need to register your own twitter app key first. The api key should be set in two files: `data-collectors/twitter/twitter.py` and `data-collectors/news/twitter/twitternews.config`. 

For collecting the news twitter data, set the news agent twitter account that you are interest under `data-collectors/news/twitter/twitternews.config`. The config file is in JSON format. Edit the `accounts` section, put the news agent display name under the node `screen_name` and the file path where your data is going to be stored under the node `path`.

Start collecting twitter data by running `python twitter.py`

### Classifier


### Visualization analysis



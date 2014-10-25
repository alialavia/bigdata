from os import listdir, path
from json import loads


def iterate_tweets(directory):
    """
    Iterates over the tweets found in the data files in given directory

    :param directory: the directory to find twitter data files in
    :type directory: str or unicode
    :return: a tweet per iteration
    :rtype: dict
    """
    for file in listdir(directory):
        if file.startswith("twitter-"):
            with open(path.join(directory, file)) as f:
                for line in f:
                    try:
                        tweet = loads(line)
                        if 'text' in tweet:
                            yield tweet
                    except ValueError, e:
                        pass

from os import listdir, path
from json import loads


def iterate_news(directory):
    """
    Iterates over the news articles found in the data files in given directory

    :param directory: the directory to find twitter data files in
    :type directory: str or unicode
    :return: a tweet per iteration
    :rtype: dict
    """
    for file in listdir(directory):
        if file.startswith("news-"):
            with open(path.join(directory, file)) as f:
                for line in f:
                    try:
                        article = loads(line)
                        if 'abstract' in article:
                            yield article
                    except ValueError, e:
                        pass

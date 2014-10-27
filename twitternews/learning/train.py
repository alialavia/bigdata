from argparse import ArgumentParser
from sklearn.linear_model import SGDClassifier
from twitternews.io import iterate_tweets
from twitternews.util import keep_progress
from itertools import izip_longest as zip_longest
from twitternews.processing import featurize_all
from pickle import dump


def main():

    # Parse command line arguments
    parser = ArgumentParser()
    parser.add_argument('-s', '--sports_directory', dest='sports_directory', type=str, required=True,
                        metavar='/path/to/sports/', help='The directory where sports data files can be found')
    parser.add_argument('-p', '--politics_directory', dest='politics_directory', type=str, required=True,
                        metavar='/path/to/politics/', help='The directory where politics data files can be found')
    parser.add_argument('-t', '--technology_directory', dest='technology_directory', type=str, required=True,
                        metavar='/path/to/technology/', help='The directory where technology data files can be found')
    parser.add_argument('-o', '--other_directory', dest='other_directory', type=str, required=False,
                        metavar='/path/to/other/', help='The directory where other data files can be found')
    parser.add_argument('-m', '--model', dest='model', type=str, required=True,
                        metavar='/path/to/model.file', help='The file to store the trained model in')
    arguments = parser.parse_args()

    # Create iterators and stochastic gradient descent classifier (L1 regularized SVM)
    sgd_classifier = SGDClassifier(alpha=1e-6, epsilon=0.1, n_jobs=4, penalty='l1', loss='modified_huber')
    classes = ['other', 'sports', 'politics', 'technology']
    sports_tweets = iterate_tweets(arguments.sports_directory)
    politics_tweets = iterate_tweets(arguments.politics_directory)
    technology_tweets = iterate_tweets(arguments.technology_directory)
    other_tweets = iterate_tweets(arguments.other_directory)
    all_tweets = zip_longest(sports_tweets, politics_tweets, technology_tweets, other_tweets)

    # Process all tweets combined
    X = []
    y = []
    for (sports_tweet, politics_tweet, technology_tweet, other_tweet) in keep_progress(all_tweets):
        if sports_tweet is not None:
            X.append(sports_tweet['text'])
            y.append('sports')
        if politics_tweet is not None:
            X.append(politics_tweet['text'])
            y.append('politics')
        if technology_tweet is not None:
            X.append(technology_tweet['text'])
            y.append('technology')
        if other_tweet is not None:
            X.append(other_tweet['text'])
            y.append('other')
        if sports_tweet is None and politics_tweet is None and technology_tweets is None:
            break

        # Perform a partial fit in batches of 1000 tweets
        if len(X) >= 1000:
            sgd_classifier.partial_fit(featurize_all(X), y, classes)
            X = []
            y = []

    # Fit remainder that was not yet processed
    if len(X) > 0:
        sgd_classifier.partial_fit(featurize_all(X), y, classes)

    # Save classifier to a file so we can use this model later
    print("Saving classifier to file")
    sgd_classifier.sparsify()
    with open(arguments.model, 'wb') as fid:
        dump(sgd_classifier, fid)


if __name__ == "__main__":
    main()

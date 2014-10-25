from argparse import ArgumentParser
from sklearn.linear_model import SGDClassifier
from twitternews.io import iterate_tweets
from twitternews.util import keep_progress
from itertools import izip_longest as zip_longest
from twitternews.processing import featurize
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
    sgd_classifier = SGDClassifier(alpha=1e-6, epsilon=0.1, n_jobs=4, penalty='l1')
    classes = ['sports', 'politics', 'technology']
    sports_tweets = iterate_tweets(arguments.sports_directory)
    politics_tweets = iterate_tweets(arguments.politics_directory)
    technology_tweets = iterate_tweets(arguments.technology_directory)
    all_tweets = zip_longest(sports_tweets, politics_tweets, technology_tweets)

    # Process all tweets combined
    for (sports_tweet, politics_tweet, technology_tweet) in keep_progress(all_tweets):
        if sports_tweet is not None:
            sgd_classifier.partial_fit(featurize(sports_tweet), ['sports'], classes)
        if politics_tweet is not None:
            sgd_classifier.partial_fit(featurize(politics_tweet), ['politics'], classes)
        if technology_tweet is not None:
            sgd_classifier.partial_fit(featurize(technology_tweet), ['technology'], classes)

    # Save classifier to a file so we can use this model later
    with open(arguments.model, 'wb') as fid:
        dump(sgd_classifier, fid)


if __name__ == "__main__":
    main()

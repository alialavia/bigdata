from argparse import ArgumentParser
from twitternews.io import iterate_tweets
from twitternews.processing import featurize_all
from twitternews.util import keep_progress, lprintln
from itertools import izip_longest as zip_longest
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import normalize
from pickle import load
import matplotlib.pyplot as plt


def confusion_matrix_plot(CM, classes, file):
    fig = plt.figure()
    subfig = fig.add_subplot(111)
    cax = subfig.matshow(CM, interpolation='nearest')
    fig.colorbar(cax)
    subfig.set_xlabel('True labels', labelpad=-386)
    subfig.set_ylabel('Predicted labels', labelpad=-2)
    subfig.set_xticklabels(['']+classes)
    subfig.set_yticklabels(['']+classes)
    plt.savefig(file, format='pdf')


def display_metrics(y, y_predicted):

    classes = ['technology', 'sports', 'politics', 'other']

    # Classification report (precision, recall, F1-score)
    print classification_report(y, y_predicted, classes)

    # Confusion matrix plot
    CM = confusion_matrix(y, y_predicted, classes).astype(float)
    CM_cols = normalize(CM, norm='l1', axis=0)
    CM_rows = normalize(CM, norm='l1', axis=1)
    confusion_matrix_plot(CM_cols, classes, 'plots/high-precision.pdf')
    confusion_matrix_plot(CM_rows, classes, 'plots/low-recall.pdf')


def main():

    # Parse command line arguments
    parser = ArgumentParser()
    parser.add_argument('-s', '--sports_directory', dest='sports_directory', type=str, required=True,
                        metavar='/path/to/sports/', help='The directory where sports data files can be found')
    parser.add_argument('-p', '--politics_directory', dest='politics_directory', type=str, required=True,
                        metavar='/path/to/politics/', help='The directory where politics data files can be found')
    parser.add_argument('-t', '--technology_directory', dest='technology_directory', type=str, required=True,
                        metavar='/path/to/technology/', help='The directory where technology data files can be found')
    parser.add_argument('-o', '--other_directory', dest='other_directory', type=str, required=True,
                        metavar='/path/to/other/', help='The directory where other data files can be found')
    parser.add_argument('-m', '--model', dest='model', type=str, required=True,
                        metavar='/path/to/model.file', help='The classification model file')
    arguments = parser.parse_args()

    # Create iterators
    sports_tweets = iterate_tweets(arguments.sports_directory)
    politics_tweets = iterate_tweets(arguments.politics_directory)
    technology_tweets = iterate_tweets(arguments.technology_directory)
    other_tweets = iterate_tweets(arguments.other_directory)
    all_tweets = zip_longest(sports_tweets, politics_tweets, technology_tweets, other_tweets)

    # Open classifier and predict labels while storing the actual labels
    with open(arguments.model, 'r') as fid:
        sgd_classifier = load(fid)
        X = []
        y = []
        y_predicted = []
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

            if len(X) >= 1000:
                y_predicted.extend(sgd_classifier.predict(featurize_all(X)))
                X = []

        if len(X) > 0:
            y_predicted.extend(sgd_classifier.predict(featurize_all(X)))

        # Perform several metrics over the predicted labels compared to the actual labels
        display_metrics(y, y_predicted)



if __name__ == "__main__":
    main()

from argparse import ArgumentParser
from twitternews.io import iterate_tweets
from twitternews.processing import featurize_all
from twitternews.util import keep_progress, lprintln
from pickle import load


def main():

    # Parse command line arguments
    parser = ArgumentParser()
    parser.add_argument('-d', '--twitter_directory', dest='twitter_directory', type=str, required=True,
                        metavar='/path/to/twitter/', help='The directory where twitter data files can be found')
    parser.add_argument('-m', '--model', dest='model', type=str, required=True,
                        metavar='/path/to/model.file', help='The classification model file')
    arguments = parser.parse_args()

    # Create iterators and stochastic gradient descent classifier (L1 regularized SVM)
    with open(arguments.model, 'r') as fid:
        sgd_classifier = load(fid)
        X = []
        count = 0
        for tweet in keep_progress(iterate_tweets(arguments.twitter_directory)):

            # Grab 2000 tweets before classifying them
            X.append(tweet['text'])
            count += 1
            if count >= 2000:
                # Convert all tweets to features
                X_f = featurize_all(X)

                # Predict labels and probability scores
                labels = sgd_classifier.predict(X_f)
                proba = sgd_classifier.predict_proba(X_f)

                # Iterate over all labels and only print out those that are not in 'other'
                for idx, label in enumerate(labels):
                    if label != 'other':
                        lprintln(label + " :: " + X[idx].encode('UTF8') + " (score:" + str(proba[idx]) + ")")
                        lprintln("")

                # Reset for next 2000 tweets
                X = []
                count = 0


if __name__ == "__main__":
    main()

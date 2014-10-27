from sklearn.feature_extraction.text import HashingVectorizer
from nltk import word_tokenize
from nltk.stem import LancasterStemmer


class Tokenizer():

    def __init__(self):
        """
        Constructs a tokenizer object
        """
        self.stemmer = LancasterStemmer()

    def __call__(self, doc):
        """
        Tokenizes text

        :param doc: the text to tokenize
        :type doc: str or unicode
        :return: a list of tokens
        :rtype: list of (str or unicode)
        """
        return [self.stemmer.stem(token) for token in word_tokenize(doc)]


hasher = HashingVectorizer(n_features=2**23,
                           tokenizer=Tokenizer(),
                           lowercase=True,
                           strip_accents='unicode',
                           stop_words='english',
                           ngram_range=(1, 4))


def featurize(text):
    """
    Processes text and generates a feature vector

    :param text: the text to process
    :type text: str or unicode
    :return: a sparse feature vector representing the text
    :rtype: :class:`scipy.sparse.csr_matrix`
    """
    return hasher.transform([text])[0]

def featurize_all(list):
    """
    Processes list and generates feature vectors for all items

    :param text: the list to process
    :type text: str or unicode
    :return: a sparse feature vector representing the text
    :rtype: :class:`scipy.sparse.csr_matrix`
    """
    return hasher.transform(list)

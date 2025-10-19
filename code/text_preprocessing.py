from nltk import word_tokenize
from nltk.corpus import stopwords
from string import punctuation

from nltk import download
download('stopwords')
download('punkt_tab')

stop_words = set(stopwords.words('english'))

def preprocess_sentence(text):
    text = text.replace('/', ' / ')
    text = text.replace('.-', ' .- ')
    text = text.replace('.', ' . ')
    text = text.replace('\'', ' \' ')
    text = text.lower()

    tokens = [token for token in word_tokenize(text) if token not in punctuation and token not in stop_words]

    return ' '.join(tokens)


import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from TextPreprocessingOperations.PorterStemmer import PorterStemmer

class TextPreprocessing:
    def __init__(self):
        self.porterStemmer = PorterStemmer()

    def preprocessText(self, text):
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = text.lower()
        return text

    def removeStopwords(self, text):
        stopWords = set(stopwords.words('english'))
        tokens = word_tokenize(text)
        filteredText = [word for word in tokens if word not in stopWords]
        return ' '.join(filteredText)

    def applyStemming(self, text):
        stemmedText = [self.porterStemmer.stem(word) for word in word_tokenize(text)]
        return ' '.join(stemmedText)
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import re

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class DataPreprocessor:
    def __init__(self):
        self.stopWords = set(stopwords.words('english'))
        self.ps = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

    def preprocessText(self, text):
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = text.lower()
        return text

    def removeStopwords(self, text):
        tokens = word_tokenize(text)
        filteredText = [word for word in tokens if word not in self.stopWords]
        return ' '.join(filteredText)

    def applyStemming(self, text):
        stemmedText = [self.ps.stem(word) for word in word_tokenize(text)]
        return ' '.join(stemmedText)

    def applyLemmatization(self, text):
        lemmatizedText = [self.lemmatizer.lemmatize(word) for word in word_tokenize(text)]
        return ' '.join(lemmatizedText)

    def preprocessDocuments(self, documents):
        preprocessedDocuments = []
        for document in documents:
            preprocessedDocument = self.preprocessText(document)
            preprocessedDocument = self.removeStopwords(preprocessedDocument)
            preprocessedDocument = self.applyStemming(preprocessedDocument)
            preprocessedDocument = self.applyLemmatization(preprocessedDocument)
            preprocessedDocuments.append(preprocessedDocument)
        return preprocessedDocuments

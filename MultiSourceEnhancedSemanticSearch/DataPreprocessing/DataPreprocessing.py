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
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(self.ps.stem(word)) for word in tokens if word not in self.stop_words]
        return tokens

    def preprocessData(self, data):
        return [self.preprocessText(text) for text in data]

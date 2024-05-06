import nltk
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD

class LSA:
    def __init__(self, text):
        self.text = text
        self.sentences = self.preprocessText(text)
        self.tf_matrix, self.terms = self.construct_tf_matrix(self.sentences)
        self.U, self.S, self.V_T = self.applySVD(self.tf_matrix)

    def preprocessText(self, text):
        sentences = sent_tokenize(text)

        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')

        stopWords = set(stopwords.words('english'))
        stemmer = PorterStemmer()
        lemmatizer = WordNetLemmatizer()

        processedSentences = []

        for sentence in sentences:
            words = word_tokenize(sentence)
            filteredWords = []

            for word in words:
                lemmaWord = lemmatizer.lemmatize(word.lower())
                if lemmaWord not in stopWords:
                    filteredWords.append(stemmer.stem(lemmaWord))

            filteredSentence = ' '.join(filteredWords)
            if filteredSentence:
                processedSentences.append(filteredSentence)

        return processedSentences

    def construct_tf_matrix(self, sentences, max_features=1000):
        vectorizer = CountVectorizer(max_features=max_features)
        tf_matrix = vectorizer.fit_transform(sentences)
        terms = vectorizer.get_feature_names_out()

        return tf_matrix, terms

    def applySVD(self, tf_matrix, n_components=100):
        svd = TruncatedSVD(n_components=n_components)
        U = svd.fit_transform(tf_matrix)
        S = svd.explained_variance_ratio_
        V_T = svd.components_

        return U, S, V_T

    def getMostSignificantSentences(self, numSentences=2):
        mostSignificantConcept = np.argmax(self.S)
        highestIndices = np.argsort(self.U[:, mostSignificantConcept])[::-1][:numSentences]
        lowestIndices = np.argsort(self.U[:, mostSignificantConcept])[:numSentences]

        highestSentences = [self.sentences[idx] for idx in highestIndices]
        lowestSentences = [self.sentences[idx] for idx in lowestIndices]

        return highestSentences, lowestSentences

    def getMostSignificantTerms(self, numTerms=5):
        mostSignificantConcept = np.argmax(self.S)
        highestIndices = np.argsort(self.V_T[mostSignificantConcept, :])[::-1][:numTerms]
        lowestIndices = np.argsort(self.V_T[mostSignificantConcept, :])[:numTerms]

        highestTerms = [self.terms[idx] for idx in highestIndices]
        lowestTerms = [self.terms[idx] for idx in lowestIndices]

        return highestTerms, lowestTerms
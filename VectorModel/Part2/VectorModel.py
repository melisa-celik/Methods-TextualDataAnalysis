from collections import defaultdict
import json
import math
import numpy as np
from sklearn.preprocessing import normalize

class VectorModel:
    def __init__(self, filePath):
        self.documents = self.loadDocuments(filePath)
        self.numDocuments = len(self.documents)
        self.termFrequency = defaultdict(lambda: defaultdict(int))
        self.inverseDocumentFrequency = {}
        self.tf_idf_weights = defaultdict(lambda: defaultdict(float))

        self.computeTermFrequencies()
        self.computeInverseDocumentFrequencies()
        self.compute_tf_idf_weights()

    def loadDocuments(self, filePath):
        with open(filePath, 'r') as file:
            data = json.load(file)
        return data

    def computeTermFrequencies(self):
        for doc in self.documents:
            docId = doc['id']
            content = doc['content']
            terms = content.lower().split()
            termCount = defaultdict(int)
            for term in terms:
                termCount[term] += 1
            self.termFrequency[docId] = dict(termCount)

    def computeInverseDocumentFrequencies(self):
        termDocumentFreq = defaultdict(int)
        for termCounts in self.termFrequency.values():
            for term in termCounts:
                termDocumentFreq[term] += 1

        for term, df_t in termDocumentFreq.items():
            self.inverseDocumentFrequency[term] = math.log(self.numDocuments / df_t)

    def compute_tf_idf_weights(self):
        for docId, termCounts in self.termFrequency.items():
            for term, tf in termCounts.items():
                idf = self.inverseDocumentFrequency[term]
                self.tf_idf_weights[docId][term] = tf * idf

    def scoreDocuments(self, queryTerms):
        queryTerms = set(queryTerms)
        scores = defaultdict(float)

        for docId, docWeights in self.tf_idf_weights.items():
            score = sum(docWeights[term] for term in queryTerms if term in docWeights)
            scores[docId] = score

        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]

    def computeDotProduct(self, vector1, vector2):
        """Compute the dot product of two vectors."""
        return sum(vector1[key] * vector2.get(key, 0) for key in vector1)

    def normalizeColumns(self, matrix):
        """Normalize the columns of a matrix."""
        return normalize(np.array(list(matrix.values())).T, axis=0).T.tolist()

    def normalizeRows(self, matrix):
        """Normalize the rows of a matrix."""
        return normalize(np.array(list(matrix.values())), axis=1).tolist()

    def findMostSimilarDocument(self, docId, use_tfidf=True):
        """Find the most similar document to a given document based on dot product."""
        queryVector = self.tf_idf_weights[docId] if use_tfidf else self.termFrequency[docId]
        similarities = {}
        for otherDocId, otherVector in self.tf_idf_weights.items():
            if otherDocId != docId:
                similarity = self.computeDotProduct(queryVector, otherVector)
                similarities[otherDocId] = similarity
        return max(similarities.items(), key=lambda x: x[1])

    def findMostSimilarWord(self, word, use_tfidf=True):
        """Find the most similar word to a given word based on dot product."""
        queryVector = {word: 1} if use_tfidf else {word: sum(self.termFrequency[docId].get(word, 0) for docId in self.termFrequency)}
        similarities = {}
        for term, vector in self.tf_idf_weights.items():
            if term != word:
                similarity = self.computeDotProduct(queryVector, vector)
                similarities[term] = similarity
        return max(similarities.items(), key=lambda x: x[1])

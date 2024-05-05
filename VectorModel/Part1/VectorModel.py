from collections import defaultdict
import json
import math

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
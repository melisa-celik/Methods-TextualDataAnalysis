from sortedcontainers import SortedList
from collections import defaultdict
from nltk.stem import PorterStemmer
import re
from InvertedIndex.CompressionTypes.Compressor import Compressor

class InvertedIndex:
    def __init__(self):
        self.invertedIndex = defaultdict(SortedList)
        self.stemmer = PorterStemmer()

    def buildIndex(self, documents):
        term_doc_pairs = []

        for docID, document in documents.items():
            terms = self.tokenize(document)
            for term in terms:
                term_doc_pairs.append((term, docID))

        term_doc_pairs.sort(key=lambda x: (x[0], x[1]))

        unique_term_doc_pairs = []
        for i in range(len(term_doc_pairs)):
            if i == 0 or term_doc_pairs[i] != term_doc_pairs[i-1]:
                unique_term_doc_pairs.append(term_doc_pairs[i])

        for term, docID in unique_term_doc_pairs:
            self.invertedIndex[term].add(docID)

    def tokenize(self, document):
        return [self.stemmer.stem(word) for word in re.findall(r'\b\w+\b', document.lower())]

    def getDocumentsForTerm(self, term):
        return self.invertedIndex.get(self.stemmer.stem(term), [])

    def printIndex(self):
        for term, docIDs in self.invertedIndex.items():
            print(term, docIDs)

    def compress(self, docIDs, method):
        if method == "gamma":
            return Compressor.gamma_encode(docIDs)
        elif method == "fibonacci":
            return Compressor.fibonacci_encode(docIDs)
        else:
            raise ValueError("Unsupported compression method. Supported methods are 'Elias Gamma' and 'Fibonacci'.")

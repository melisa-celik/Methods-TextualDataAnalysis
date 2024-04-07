import re
from collections import defaultdict
from nltk.stem import PorterStemmer

class InvertedIndex:
    def __init__(self):
        self.invertedIndex = defaultdict(list)
        self.stemmer = PorterStemmer()

    def buildIndex(self, documents):
        for docID, document in documents.items():
            terms = self.tokenize(document)
            for term in terms:
                self.invertedIndex[term].append(docID)

    def tokenize(self, document):
        return [self.stemmer.stem(word) for word in re.findall(r'\b\w+\b', document.lower())]

    def getDocumentsForTerm(self, term):
        return self.invertedIndex.get(self.stemmer.stem(term), [])

    def printIndex(self):
        for term, docIDs in self.invertedIndex.items():
            print(term, docIDs)

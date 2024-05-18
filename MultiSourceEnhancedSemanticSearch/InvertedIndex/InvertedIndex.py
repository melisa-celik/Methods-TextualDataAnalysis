from collections import defaultdict

class InvertedIndex:
    def __init__(self):
        self.invertedIndex = defaultdict(list)

    def buildInvertedIndex(self, documents):
        for docID, document in enumerate(documents):
            for term in document:
                self.invertedIndex[term].append(docID)
        return self.invertedIndex

    def getDocumentsForTerm(self, term):
        return self.invertedIndex[term] if term in self.invertedIndex else []

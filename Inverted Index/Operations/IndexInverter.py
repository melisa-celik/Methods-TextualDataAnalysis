class InvertedIndex:
    def __init__(self):
        self.inverted_index = {}

    def addDocument(self, docID, text):
        terms = self.tokenize(text)
        for term in terms:
            if term not in self.inverted_index:
                self.inverted_index[term] = set()
            self.inverted_index[term].add(docID)

    def tokenize(self, text):
        return text.split()

    def buildIndex(self, documents):
        for docID, text in documents.items():
            self.addDocument(docID, text)

    def getDocumentsForTerm(self, term):
        return self.inverted_index.get(term, set())

    def search(self, query):
        query_terms = self.tokenize(query)
        relevant_docs = set()
        for term in query_terms:
            relevant_docs = relevant_docs.union(self.getDocumentsForTerm(term))
        return relevant_docs

    def printIndex(self):
        for term, docIDs in self.inverted_index.items():
            print(term, docIDs)



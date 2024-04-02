class QuerySystem:
    def __init__(self, index_inverter):
        self.inverted_index = index_inverter

    def processQuery(self, query):
        terms = query.split(" AND ")
        if len(terms) == 1:
            return self.inverted_index.getDocumentsForTerm(terms[0])

        documents = self.inverted_index.getDocumentsForTerm(terms[0])
        for term in terms[1:]:
            documents = self.intersect(documents, self.inverted_index.getDocumentsForTerm(term))
            if not documents:
                print("No documents found for query")

        return documents

    def intersect(self, set1, set2):
        return set1.intersection(set2)

    def printIndex(self):
        self.inverted_index.printIndex()

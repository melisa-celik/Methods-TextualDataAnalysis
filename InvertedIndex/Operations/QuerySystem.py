from nltk.stem import PorterStemmer

class QuerySystem:
    def __init__(self, inverted_index):
        self.invertedIndex = inverted_index
        self.stemmer = PorterStemmer()

    def processQuery(self, query):
        query = query.lower()
        if " and " in query:
            return self.processAndQuery(query)
        elif " or " in query:
            return self.processOrQuery(query)
        else:
            return self.processIndividualTerms(query)

    def processAndQuery(self, query):
        terms = [self.stemmer.stem(term) for term in query.split(" and ")]
        term_sets = [set(self.invertedIndex.getDocumentsForTerm(term)) for term in terms]
        return set.intersection(*term_sets)

    def processOrQuery(self, query):
        terms = [self.stemmer.stem(term) for term in query.split(" or ")]
        term_sets = [set(self.invertedIndex.getDocumentsForTerm(term)) for term in terms]
        return set.union(*term_sets)

    def processIndividualTerms(self, query):
        term = self.stemmer.stem(query)
        return set(self.invertedIndex.getDocumentsForTerm(term))

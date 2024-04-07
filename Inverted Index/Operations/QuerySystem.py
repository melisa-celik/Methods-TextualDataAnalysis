from nltk.stem import PorterStemmer

class QuerySystem:
    def __init__(self, inverted_index):
        self.invertedIndex = inverted_index
        self.stemmer = PorterStemmer()

    def processQuery(self, query):
        if " AND " in query or " and " in query:
            return self.processAndQuery(query)
        elif " OR " in query or " or " in query:
            return self.processOrQuery(query)
        else:
            return self.processIndividualTerms(query)

    def processAndQuery(self, query):
        terms = query.replace(" and ", " AND ").split(" AND ")
        termSets = [set(self.invertedIndex.getDocumentsForTerm(self.stemmer.stem(term))) for term in terms]
        result = termSets[0].intersection(*termSets[1:])
        return result

    def processOrQuery(self, query):
        terms = query.replace(" or ", " OR ").split(" OR ")
        termSets = [set(self.invertedIndex.getDocumentsForTerm(self.stemmer.stem(term))) for term in terms]
        result = set().union(*termSets)
        return result

    def processIndividualTerms(self, query):
        terms = query.split()
        stemmedTerms = [self.stemmer.stem(term.lower()) for term in terms]
        matchingDocs = set()
        for term in stemmedTerms:
            matchingDocs.update(self.invertedIndex.getDocumentsForTerm(term))
        return matchingDocs
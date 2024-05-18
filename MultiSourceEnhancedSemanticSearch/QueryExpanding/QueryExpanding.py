from nltk.corpus import wordnet

class QueryExpander:
    def __init__(self, dataPreprocessor):
        self.dataPreprocessor = dataPreprocessor

    def getSynonyms(self, word):
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
        return synonyms

    def expandQuery(self, query):
        queryTokens = self.dataPreprocessor.preprocessText(query)
        expandedQuery = set(queryTokens)
        for token in queryTokens:
            synonyms = self.getSynonyms(token)
            # expandedQuery = expandedQuery.union(synonyms)
            expandedQuery.update(synonyms)
        return list(expandedQuery)
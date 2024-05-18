from flask import Flask, request, render_template, redirect, url_for, session
from MultiSourceEnhancedSemanticSearch.ClusteringAndTopicModeling.DocumentClustering.DocumentClustering import DocumentClusterer
from MultiSourceEnhancedSemanticSearch.ClusteringAndTopicModeling.TopicModeling.TopicModeling import TopicModeler
from MultiSourceEnhancedSemanticSearch.DataPreprocessing.DataPreprocessing import DataPreprocessor
from MultiSourceEnhancedSemanticSearch.GeneratingEmbeddings.GeneratingEmbeddings import EmbeddingGenerator
from MultiSourceEnhancedSemanticSearch.InvertedIndex.InvertedIndex import InvertedIndex
from MultiSourceEnhancedSemanticSearch.QueryExpanding.QueryExpanding import QueryExpander
from MultiSourceEnhancedSemanticSearch.SemanticSearch.SemanticSearch import SemanticSearch
from MultiSourceEnhancedSemanticSearch.System.RecommenderSystem.RecommenderSystem import RecommenderSystem
from MultiSourceEnhancedSemanticSearch.System.RecommenderSystem.RecommendEvaluation import RecommendEvaluator
from MultiSourceEnhancedSemanticSearch.System.User.User import User
from MultiSourceEnhancedSemanticSearch.System.User.Security import UserAuthenticator
from MultiSourceEnhancedSemanticSearch.System.WebServer.WebServer import WebInterface

documents = [
    "Natural language processing (NLP) is a field of artificial intelligence.",
    "It focuses on the interaction between computers and humans through natural language.",
    "The ultimate objective of NLP is to read, decipher, understand, and make sense of human languages.",
    "Most NLP techniques rely on machine learning to derive meaning from human languages.",
    "NLP is used to apply algorithms to identify and extract information from textual data and speech.",
    "Natural language processing helps computers communicate with humans in their own language and scales other language-related tasks.",
    "For example, NLP makes it possible for computers to read text, hear speech, interpret it, measure sentiment and determine which parts are important.",
    "NLP involves several challenges such as natural language understanding, natural language generation, natural language translation, and natural language acquisition.",
    "Natural language processing is used to apply algorithms to identify and extract information from textual data and speech.",
    "Natural language processing helps computers communicate with humans in their own language.",
    "Natural language processing involves several challenges such as natural language understanding, natural language generation, natural language translation, and natural language acquisition."
]

dataPreprocessor = DataPreprocessor()
invertedIndex = InvertedIndex()
embeddingGenerator = EmbeddingGenerator()
semanticSearch = SemanticSearch(embeddingGenerator, dataPreprocessor)
queryExpander = QueryExpander(dataPreprocessor)
documentClusterer = DocumentClusterer(numClusters=3)
topicModeler = TopicModeler()
recommenderSystem = RecommenderSystem(embeddingGenerator)
user = User("cel0052", "Melisa Çelik", "melisa.celik.st@vsb.cz", "celik12345")
userAuthenticator = UserAuthenticator()
userAuthenticator.register(user.userID, user.name, user.email, user.password)
recommendEvaluator = RecommendEvaluator(recommenderSystem, user.userID)
webInterface = WebInterface(semanticSearch, documentClusterer)
app = Flask(__name__)

def searchWithInvertedIndex(query):
    expandedQuery = queryExpander.expandQuery(query)
    documentEmbeddings = EmbeddingGenerator().generateEmbeddings(documents)
    docIDs = set()
    for term in expandedQuery:
        docIDs.update(invertedIndex.getDocumentsForTerm(term))

    relevantDocumentEmbeddings = [documentEmbeddings[docID] for docID in docIDs]
    relevantDocuments = [documents[docID] for docID in docIDs]

    top_k_indices, similarities = semanticSearch.search(query, relevantDocumentEmbeddings)
    return [(relevantDocuments[i], similarities[i]) for i in top_k_indices]


@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = searchWithInvertedIndex(query)
    return render_template('results.html', results=results)

def main():
    preprocessedDocuments = dataPreprocessor.preprocessData(documents)
    index = invertedIndex.buildInvertedIndex(preprocessedDocuments)
    docEmbeddings = embeddingGenerator.generateEmbeddings(preprocessedDocuments)
    clusters = documentClusterer.clusterDocuments(docEmbeddings)
    topics = topicModeler.model(preprocessedDocuments)

    webInterface.prepareVisualizationData(docEmbeddings, clusters)
    app.run()

if __name__ == "__main__":
    main()




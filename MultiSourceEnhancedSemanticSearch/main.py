from flask import Flask , request, render_template, redirect, url_for, session
import plotly.express as px
import logging
import pandas as pd
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

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def loadDocuments(file_path):
    with open(file_path, 'r') as file:
        documents = file.readlines()
    return [doc.strip() for doc in documents]

documents = loadDocuments(r"C:\Users\Lenovo\PycharmProjects\Methods-TextualDataAnalysis\MultiSourceEnhancedSemanticSearch\Data\documents.txt")

logger.debug("Initializing Components...")
dataPreprocessor = DataPreprocessor()
invertedIndex = InvertedIndex()
embeddingGenerator = EmbeddingGenerator()
semanticSearch = SemanticSearch(embeddingGenerator, dataPreprocessor)
queryExpander = QueryExpander(dataPreprocessor)
topicModeler = TopicModeler()
recommenderSystem = RecommenderSystem(embeddingGenerator)

logging.debug("Creating User...")
user = User("cel0052", "Melisa Çelik", "melisa.celik.st@vsb.cz", "celik12345")
logging.debug("Authenticating User...")
userAuthenticator = UserAuthenticator()

try:
    userAuthenticator.register(user.userID, user.name, user.email, user.password)
except ValueError as e:
    print(e)

recommendEvaluator = RecommendEvaluator(recommenderSystem, user.userID)
app = Flask(__name__, template_folder=r"C:\Users\Lenovo\PycharmProjects\Methods-TextualDataAnalysis\MultiSourceEnhancedSemanticSearch\System\WebServer\HTMLFiles")
app.secret_key = '23042001'

preprocessedDocuments = dataPreprocessor.preprocessData(documents)
preprocessedDocumentsAsStrings = [" ".join(doc) for doc in preprocessedDocuments]  # Convert tokenized docs to strings
docEmbeddings = embeddingGenerator.generateEmbeddings(preprocessedDocuments)
topics, numTopics = topicModeler.model(preprocessedDocumentsAsStrings)
documentClusterer = DocumentClusterer(numClusters=numTopics)
clusters = documentClusterer.clusterDocuments(docEmbeddings)
webInterface = WebInterface(semanticSearch, documentClusterer)

# @app.route('/search', methods=['POST'])
# def search():
#     query = request.form['query']
#     results = searchWithInvertedIndex(query)
#     return render_template('results.html', results=results)

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
    logger.debug(f"Search query: {query}")
    top_k_indices, similarities = semanticSearch.search(query, docEmbeddings)
    results = [{"document": documents[i], "similarity": f"{similarity:.4f}"} for i, similarity in zip(top_k_indices, similarities)]

    queryTokens = dataPreprocessor.preprocessText(query)
    queryTopicIndex = topicModeler.topicModel.transform([" ".join(queryTokens)])[0]
    queryTopic = topicModeler.topicModel.get_topic(queryTopicIndex)

    return render_template('results.html', results=results, queryTopic=queryTopic)

@app.route('/visualize', methods=['GET'])
def visualize():
    logger.debug("Generating Visualization...")
    visualizationData = pd.DataFrame(docEmbeddings)
    visualizationData['Cluster'] = clusters
    fig = px.scatter(visualizationData, x=0, y=1, color='Cluster', title='Document Clusters')
    graph = fig.to_html(full_html=False)
    return render_template('visualize.html', graph=graph)

@app.route('/')
def index():
    if 'userID' in session:
        logger.debug(f"User {session['userID']} is logged in.")
        return render_template('index.html', userID=session['userID'])
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userID = request.form['userID']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        logger.debug(f"Registering user: {userID}, {name}, {email}")
        try:
            userAuthenticator.register(userID, name, email, password)
            return redirect(url_for('login'))
        except ValueError as e:
            return str(e)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userID = request.form['userID']
        password = request.form['password']
        logger.debug(f"Login attempt for user: {userID}")
        result = userAuthenticator.login(userID, password)
        if result == "Login successful":
            session['userID'] = userID
            logger.debug(f"Login successful for user: {userID}")
            return redirect(url_for('index'))
        logger.debug(f"Login failed for user: {userID}")
        return result
    return render_template('login.html')

@app.route('/logout')
def logout():
    logger.debug(f"User {session.get('userID')} logging out.")
    session.pop('userID', None)
    return redirect(url_for('login'))

@app.route('/recommend', methods=['GET'])
def recommend():
    userHistory = [0, 1, 2]
    logger.debug(f"Generating recommendations for user history: {userHistory}")
    recommendedIndices, similarities = recommenderSystem.recommendDocuments(userHistory, docEmbeddings)
    recommendations = [{"document": documents[i], "similarity": f"{similarity:.4f}"} for i, similarity in zip(recommendedIndices, similarities)]

    groundTruth = [1 if i in userHistory else 0 for i in range(len(documents))]
    predictions = [1 if i in recommendedIndices else 0 for i in range(len(documents))]

    precision, recall, f1 = recommendEvaluator.evaluate(groundTruth, predictions)

    logger.debug(f"Recommendations: {recommendations}")
    logger.debug(f"Evaluation - Precision: {precision}, Recall: {recall}, F1: {f1}")
    return render_template('recommendations.html', recommendations=recommendations, precision=precision, recall=recall, f1=f1)


def main():
    logger.debug("Initializing General Operations...")
    preprocessedDocuments = dataPreprocessor.preprocessData(documents)
    preprocessedDocumentsAsStrings = [" ".join(doc) for doc in preprocessedDocuments]
    global docEmbeddings, clusters
    index = invertedIndex.buildInvertedIndex(preprocessedDocuments)
    docEmbeddings = embeddingGenerator.generateEmbeddings(preprocessedDocuments)
    clusters = documentClusterer.clusterDocuments(docEmbeddings)
    topics, numTopics = topicModeler.model(preprocessedDocumentsAsStrings)

    webInterface.prepareVisualizationData(docEmbeddings, clusters)

    logger.debug("Initialization complete. Starting Flask app.")
    app.run(debug=True, port=5000)

if __name__ == "__main__":
    main()
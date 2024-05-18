from flask import Flask, request, render_template, redirect, url_for, session
import plotly.express as px
import pandas as pd
from MultiSourceEnhancedSemanticSearch.System.User.Security import UserAuthenticator
from MultiSourceEnhancedSemanticSearch.SemanticSearch.SemanticSearch import SemanticSearch
from MultiSourceEnhancedSemanticSearch.ClusteringAndTopicModeling.DocumentClustering.DocumentClustering import DocumentClusterer
from MultiSourceEnhancedSemanticSearch.GeneratingEmbeddings.GeneratingEmbeddings import EmbeddingGenerator
from MultiSourceEnhancedSemanticSearch.DataPreprocessing.DataPreprocessing import DataPreprocessor

app = Flask(__name__, template_folder=r"C:\Users\Lenovo\PycharmProjects\Methods-TextualDataAnalysis\MultiSourceEnhancedSemanticSearch\System\WebServer\HTMLFiles")
app.secret_key = '23042001'

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

authentication = UserAuthenticator()
dataPreprocessor = DataPreprocessor()
embeddingGenerator = EmbeddingGenerator()
semanticSearch = SemanticSearch(embeddingGenerator, dataPreprocessor)
documentClusterer = DocumentClusterer()
documentEmbeddings = semanticSearch.embeddingsGenerator.generateEmbeddings(documents)
clusters = documentClusterer.clusterDocuments(documentEmbeddings)

class WebInterface:
    def __init__(self, semanticSearch, documentClusterer):
        self.semanticSearch = semanticSearch
        self.documentClusterer = documentClusterer

    def prepareVisualizationData(self, docEmbeddings, clusters):
        df = pd.DataFrame(docEmbeddings)
        df['Cluster'] = clusters
        return df

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    top_k_indices, similarities = semanticSearch.search(query, documentEmbeddings, top_k=5)
    results = [{"document": documents[i], "similarity": f"{similarity:.4f}"} for i, similarity in zip(top_k_indices, similarities)]
    return render_template('results.html', results=results)

@app.route('/visualize', methods=['POST'])
def visualize():
    visualizationData = WebInterface.prepareVisualizationData(documentEmbeddings, clusters)
    fig = px.scatter(visualizationData, x=0, y=1, color='Cluster', title='Document Clusters')
    graph = fig.to_html(full_html=False)
    return render_template('visualization.html', graph=graph)

@app.route('/')
def index():
    if 'userID' in session:
        return render_template('index.html', userID=session['userID'])
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userID = request.form['userID']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        try:
            authentication.register(userID, name, email, password)
            return redirect(url_for('login'))
        except ValueError as e:
            return str(e)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userID = request.form['userID']
        password = request.form['password']
        result = authentication.login(userID, password)
        if result == "Login successful":
            session['userID'] = userID
            return redirect(url_for('index'))
        return result
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('userID', None)
    return redirect(url_for('login'))

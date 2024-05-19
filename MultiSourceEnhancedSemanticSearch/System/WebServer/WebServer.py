import logging
from flask import Flask, request, render_template, redirect, url_for, session
import plotly.express as px
import pandas as pd


class WebInterface:
    def __init__(self, semanticSearch, documentClusterer):
        self.semanticSearch = semanticSearch
        self.documentClusterer = documentClusterer

    def prepareVisualizationData(self, docEmbeddings, clusters):
        df = pd.DataFrame(docEmbeddings)
        df['Cluster'] = clusters
        return df

# @app.route('/search', methods=['POST'])
# def search():
#     query = request.form['query']
#     top_k_indices, similarities = semanticSearch.search(query, documentEmbeddings, top_k=5)
#     results = [{"document": documents[i], "similarity": f"{similarity:.4f}"} for i, similarity in zip(top_k_indices, similarities)]
#     return render_template('results.html', results=results)
#
# @app.route('/visualize', methods=['POST'])
# def visualize():
#     visualizationData = WebInterface.prepareVisualizationData(documentEmbeddings, clusters)
#     fig = px.scatter(visualizationData, x=0, y=1, color='Cluster', title='Document Clusters')
#     graph = fig.to_html(full_html=False)
#     return render_template('visualization.html', graph=graph)
#
# @app.route('/')
# def index():
#     if 'userID' in session:
#         return render_template('index.html', userID=session['userID'])
#     return redirect(url_for('login'))
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         userID = request.form['userID']
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
#         try:
#             authentication.register(userID, name, email, password)
#             return redirect(url_for('login'))
#         except ValueError as e:
#             return str(e)
#     return render_template('register.html')
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         userID = request.form['userID']
#         password = request.form['password']
#         result = authentication.login(userID, password)
#         if result == "Login successful":
#             session['userID'] = userID
#             return redirect(url_for('index'))
#         return result
#     return render_template('login.html')
#
# @app.route('/logout')
# def logout():
#     session.pop('userID', None)
#     return redirect(url_for('login'))

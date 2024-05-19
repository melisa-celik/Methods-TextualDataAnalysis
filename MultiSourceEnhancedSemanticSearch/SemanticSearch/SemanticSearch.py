from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SemanticSearch:
    def __init__(self, embeddingsGenerator, dataPreprocessor):
        self.embeddingsGenerator = embeddingsGenerator
        self.dataPreprocessor = dataPreprocessor

    def search(self, query, docEmbeddings, top_k=5):
        queryTokens = self.dataPreprocessor.preprocessText(query)
        queryEmbedding = self.embeddingsGenerator.generateEmbeddings([queryTokens])[0]
        similarities = cosine_similarity([queryEmbedding], docEmbeddings)[0]
        top_k_indices = np.argsort(similarities)[-top_k:][::-1]
        top_k_indices = top_k_indices.tolist()
        return top_k_indices, similarities[top_k_indices]
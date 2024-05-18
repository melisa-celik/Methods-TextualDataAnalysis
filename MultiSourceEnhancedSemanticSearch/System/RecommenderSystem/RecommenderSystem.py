from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RecommenderSystem:
    def __init__(self, embeddingGenerator):
        self.embeddingGenerator = embeddingGenerator

    def recommend_documents(self, userHistory, docEmbeddings, top_k=5):
        userEmbeddings = [docEmbeddings[i].numpy() for i in userHistory]
        avgUserEmbedding = np.mean(userEmbeddings, axis=0)
        similarities = cosine_similarity([avgUserEmbedding], docEmbeddings)[0]
        recommendedIndices = np.argsort(similarities)[-top_k:][::-1]
        return recommendedIndices, similarities[recommendedIndices]
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import numpy as np

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

class TopicModeler:
    def __init__(self):
        self.topicModel = BERTopic(embedding_model=embedding_model)

    def model(self, documents, embeddings):
        if not all(isinstance(doc, str) for doc in documents):
            raise ValueError("All documents must be strings")
        if not isinstance(embeddings, np.ndarray):
            embeddings = np.array(embeddings)
        topics, probs = self.topicModel.fit_transform(documents, embeddings)
        numTopics = len(set(topics))
        return topics, numTopics

    def get_topic(self, query):
        queryTopic = self.topicModel.transform([query])[0]
        topicInfo = self.topicModel.get_topic(queryTopic[0])
        return topicInfo
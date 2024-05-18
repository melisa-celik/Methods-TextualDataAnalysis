from bertopic import BERTopic

class TopicModeler:
    def __init__(self):
        self.topicModel = BERTopic()

    def model(self, documents):
        topics, probs = self.topicModel.fit_transform([" ".join(document) for document in documents])
        numTopics = len(set(topics))
        return topics, numTopics
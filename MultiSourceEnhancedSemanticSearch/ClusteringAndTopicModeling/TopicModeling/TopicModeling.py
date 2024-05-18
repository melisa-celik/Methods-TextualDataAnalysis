from bertopic import BERTopic

class TopicModeler:
    def __init__(self):
        self.topicModel = BERTopic()

    def model(self, documents):
        topics, _ = self.topicModel.fit_transform([" ".join(document) for document in documents])
        return topics
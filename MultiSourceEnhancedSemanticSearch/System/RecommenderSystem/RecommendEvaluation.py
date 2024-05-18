from sklearn.metrics import precision_score, recall_score, f1_score

class RecommendEvaluator:
    def __init__(self, recommenderSystem, userID):
        self.recommenderSystem = recommenderSystem
        # self.data = data
        self.userID = userID

    def evaluate(self, groundTruth, predictions):
        # groundTruth = self.data[self.userID][groundTruth]
        precision = precision_score(groundTruth, predictions)
        recall = recall_score(groundTruth, predictions)
        f1 = f1_score(groundTruth, predictions)
        return precision, recall, f1
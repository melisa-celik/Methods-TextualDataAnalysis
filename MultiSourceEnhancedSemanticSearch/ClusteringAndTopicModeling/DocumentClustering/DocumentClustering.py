from sklearn.cluster import KMeans

class DocumentClusterer:
    def __init__(self, numClusters=3):
        self.numClusters = numClusters

    def clusterDocuments(self, docEmbeddings):
        kmeans = KMeans(n_clusters=self.numClusters)
        clusters = kmeans.fit_predict([embedding for embedding in docEmbeddings])
        return clusters

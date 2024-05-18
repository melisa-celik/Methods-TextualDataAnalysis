from sklearn.cluster import KMeans

class DocumentClusterer:
    def __init__(self, numClusters):
        self.numClusters = numClusters

    def clusterDocuments(self, docEmbeddings):
        if self.numClusters is None:
            raise ValueError("Number of clusters must be specified.")
        kmeans = KMeans(n_clusters=self.numClusters, random_state=1)
        clusters = kmeans.fit_predict([embedding for embedding in docEmbeddings])
        return clusters

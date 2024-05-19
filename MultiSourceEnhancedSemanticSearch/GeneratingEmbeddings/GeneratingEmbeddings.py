from transformers import BertTokenizer, BertModel
import torch
import numpy as np

class EmbeddingGenerator:
    def __init__(self, modelName='sentence-transformers/all-MiniLM-L6-v2'):
        self.tokenizer = BertTokenizer.from_pretrained(modelName)
        self.model = BertModel.from_pretrained(modelName)
        self.model.eval()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    def generateEmbeddings(self, documents):
        embeddings = []
        for document in documents:
            inputs = self.tokenizer(document, return_tensors='pt', padding=True, truncation=True, max_length=512).to(self.device)
            with torch.no_grad():
                outputs = self.model(**inputs)
            embedding = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
            embeddings.append(embedding)
        return np.array(embeddings)

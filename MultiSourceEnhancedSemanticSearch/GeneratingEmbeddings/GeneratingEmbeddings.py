from transformers import BertTokenizer, BertModel
import torch
from MultiSourceEnhancedSemanticSearch.DataPreprocessing.DataPreprocessing import DataPreprocessor

class EmbeddingGenerator:
    def __init__(self, modelName='bert-base-uncased'):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained(modelName)
        self.model.eval()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    def generateEmbeddings(self, documnets):
        embeddings = []
        for document in documnets:
            inputs = self.tokenizer(" ".join(document), return_tensors='pt', padding=True, truncation=True, max_length=512).to(self.device)
            with torch.no_grad():
                outputs = self.model(**inputs)
            embeddings.append(outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy())
        return embeddings


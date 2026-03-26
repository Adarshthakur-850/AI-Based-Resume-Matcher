from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Matcher:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def get_embedding(self, text):
        return self.model.encode(text)

    def compute_similarity(self, text1, text2):
        emb1 = self.get_embedding(text1).reshape(1, -1)
        emb2 = self.get_embedding(text2).reshape(1, -1)
        return cosine_similarity(emb1, emb2)[0][0]

import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer

class DenseEmbedder:
    """
    Metinleri vektör uzayına taşıyan Dense Embedding sınıfı.
    Hafif ve etkili multilingual bir model (all-MiniLM-L6-v2 veya bge-m3 benzeri) kullanır.
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> np.ndarray:
        return self.model.encode(text, convert_to_numpy=True)

    def embed_documents(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, convert_to_numpy=True)

from typing import List, Dict, Any
from sentence_transformers import CrossEncoder

class CrossEncoderReranker:
    """
    Aday dokümanları sorgu ile yan yana koyarak çapraz sorgulayan yüksek hassasiyetli Reranker.
    """
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, candidate_results: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
        if not candidate_results:
            return []

        # (Sorgu, Doküman İçeriği) çiftleri oluşturulur
        pairs = [(query, item["document"]["content"]) for item in candidate_results]
        scores = self.model.predict(pairs)

        reranked = []
        for idx, score in enumerate(scores):
            item = candidate_results[idx].copy()
            item["rerank_score"] = float(score)
            reranked.append(item)

        # Rerank skoruna göre büyükten küçüğe sırala
        reranked.sort(key=lambda x: x["rerank_score"], reverse=True)
        
        for rank, item in enumerate(reranked[:top_k], start=1):
            item["final_rank"] = rank

        return reranked[:top_k]

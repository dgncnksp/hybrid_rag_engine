from typing import List, Dict, Any
from rank_bm25 import BM25Okapi

class SparseBM25Search:
    """
    Tam kelime ve terim eşleşmelerini (TRX, USDT, 2FA vb.) yakalamak için BM25 Arama Katmanı.
    """
    def __init__(self, documents: List[Dict[str, Any]]):
        self.documents = documents
        # Basit bir kelime bölme (tokenization) stratejisi
        self.corpus = [doc["content"].lower().split() for doc in documents]
        self.bm25 = BM25Okapi(self.corpus)

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        
        # Skorlara göre indeksleri sırala
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                "document": self.documents[idx],
                "sparse_score": float(scores[idx]),
                "rank": len(results) + 1
            })
        return results

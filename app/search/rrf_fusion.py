from typing import List, Dict, Any

class RRFFusion:
    """
    Dense ve Sparse arama sonuçlarını sıralamalarına göre harmanlayan RRF Motoru.
    Formül: RRF_Score = Sum(1 / (k + rank))
    """
    def __init__(self, k: int = 60):
        self.k = k

    def combine_results(
        self, 
        dense_results: List[Dict[str, Any]], 
        sparse_results: List[Dict[str, Any]], 
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        scores: Dict[str, float] = {}
        doc_map: Dict[str, Dict[str, Any]] = {}

        # Dense sıralamaları ekle
        for item in dense_results:
            doc_id = item["document"]["id"]
            doc_map[doc_id] = item["document"]
            scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (self.k + item["rank"]))

        # Sparse (BM25) sıralamaları ekle
        for item in sparse_results:
            doc_id = item["document"]["id"]
            doc_map[doc_id] = item["document"]
            scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (self.k + item["rank"]))

        # RRF skoruna göre yeniden sırala
        sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)[:top_k]

        fused_results = []
        for rank, doc_id in enumerate(sorted_ids, start=1):
            fused_results.append({
                "document": doc_map[doc_id],
                "rrf_score": scores[doc_id],
                "rank": rank
            })
        return fused_results

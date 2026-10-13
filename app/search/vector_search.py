import numpy as np
from typing import List, Dict, Any
from app.core.embedder import DenseEmbedder

class DenseVectorSearch:
    def __init__(self, documents: List[Dict[str, Any]], embedder: DenseEmbedder):
        self.documents = documents
        self.embedder = embedder
        contents = [doc["content"] for doc in documents]
        self.doc_embeddings = self.embedder.embed_documents(contents)

    def search(self, query: str, user_role: str = "GUEST", top_k: int = 5) -> List[Dict[str, Any]]:
        query_embedding = self.embedder.embed_text(query)
        
        norm_query = query_embedding / np.linalg.norm(query_embedding)
        norm_docs = self.doc_embeddings / np.linalg.norm(self.doc_embeddings, axis=1, keepdims=True)
        similarities = np.dot(norm_docs, norm_query)
        
        # Rol Hiyerarşisi (GUEST < ANALYST < ADMIN)
        role_hierarchy = {"GUEST": 1, "ANALYST": 2, "ADMIN": 3}
        user_level = role_hierarchy.get(user_role, 1)

        results = []
        # Skorlara göre sırala
        sorted_indices = np.argsort(similarities)[::-1]
        
        for idx in sorted_indices:
            doc = self.documents[idx]
            doc_required_level = role_hierarchy.get(doc.get("required_role", "GUEST"), 1)
            
            # Metadata Filtering: Kullanıcının yetkisi yetiyorsa sonuçlara ekle
            if user_level >= doc_required_level:
                results.append({
                    "document": doc,
                    "dense_score": float(similarities[idx]),
                    "rank": len(results) + 1
                })
                if len(results) >= top_k:
                    break
        return results

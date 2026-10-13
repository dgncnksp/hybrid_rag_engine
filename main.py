from app.data.documents import SAMPLE_DOCUMENTS
from app.core.embedder import DenseEmbedder
from app.core.reranker import CrossEncoderReranker
from app.search.bm25_search import SparseBM25Search
from app.search.vector_search import DenseVectorSearch
from app.search.rrf_fusion import RRFFusion
from app.security.pii_masker import PIIMasker

def run_secured_pipeline(query: str, user_role: str):
    print(f"\n==================================================")
    print(f"Gelen Sorgu: '{query}'")
    print(f"Kullanıcı Rolü: [{user_role}]")
    print(f"==================================================")

    # 1. PII Maskeleme
    pii_masker = PIIMasker()
    clean_query = pii_masker.mask(query)
    print(f"[PII MASKED QUERY]: '{clean_query}'")

    # 2. Servislerin Başlatılması
    embedder = DenseEmbedder()
    vector_search = DenseVectorSearch(SAMPLE_DOCUMENTS, embedder)
    bm25_search = SparseBM25Search(SAMPLE_DOCUMENTS)
    rrf_fusion = RRFFusion(k=60)
    reranker = CrossEncoderReranker()

    # 3. Permission-Aware Vector Search (Metadata Filtering)
    dense_res = vector_search.search(clean_query, user_role=user_role, top_k=5)
    
    # Simple BM25 Filter Strategy for roles
    sparse_res = bm25_search.search(clean_query, top_k=5)
    role_hierarchy = {"GUEST": 1, "ANALYST": 2, "ADMIN": 3}
    filtered_sparse_res = [
        item for item in sparse_res 
        if role_hierarchy.get(user_role, 1) >= role_hierarchy.get(item["document"].get("required_role", "GUEST"), 1)
    ]

    # 4. RRF Fusion & Rerank
    fused_res = rrf_fusion.combine_results(dense_res, filtered_sparse_res, top_k=5)
    final_docs = reranker.rerank(clean_query, fused_res, top_k=2)

    print("\n--- [YETKİLENDİRİLMİŞ VE FİLTRELENMİŞ SONUÇLAR] ---")
    for doc in final_docs:
        print(f"Sıra: {doc['final_rank']} | Score: {doc['rerank_score']:.4f} | Gerekli Rol: [{doc['document']['required_role']}]")
        print(f"Başlık: {doc['document']['title']}")
        print(f"İçerik: {doc['document']['content']}\n")

if __name__ == "__main__":
    # Test 1: PII İçeren ve GUEST rolünde VIP Çekim Limiti Sorgusu
    test_query = "Benim TCKN 12345678901 ve e-postam test@example.com, VIP müşteri çekim limitleri nedir?"
    
    print(">>> DUMMY TEST 1: GUEST Rolü ile Sorgulama <<<")
    run_secured_pipeline(test_query, user_role="GUEST")

    print("\n>>> DUMMY TEST 2: ANALYST Rolü ile Sorgulama <<<")
    run_secured_pipeline(test_query, user_role="ANALYST")

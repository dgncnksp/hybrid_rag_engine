from typing import List, Dict, Any

SAMPLE_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "id": "doc_001",
        "title": "Bitcoin Transfer Süreleri ve Ağ Ücretleri",
        "content": "Bitcoin (BTC) ağında transfer süreleri blok yoğunluğuna bağlı olarak değişir. Ort. 10-30 dk.",
        "required_role": "GUEST"
    },
    {
        "id": "doc_002",
        "title": "TRX (Tron) Ağı Üzerinden USDT Transferi",
        "content": "TRX ağı (TRC-20) üzerinden yapılan USDT transferleri 1-3 dakika sürer.",
        "required_role": "GUEST"
    },
    {
        "id": "doc_003",
        "title": "VIP Müşteri Kripto Çekim Limitleri ve Muafiyetler",
        "content": "VIP Seviye 3 müşteriler için günlük çekim limiti 5.000.000 USDT'ye kadar çıkarılmıştır ve özel komisyon indirimi uygulanır.",
        "required_role": "ANALYST"
    },
    {
        "id": "doc_004",
        "title": "Sistem Mimarisi ve Soğuk Cüzdan (Cold Storage) Ağ Geçitleri",
        "content": "Hassas soğuk cüzdan transfer onayları HSM (Hardware Security Module) cihazları ve 3/5 çoklu imza (multisig) ile gerçekleşir.",
        "required_role": "ADMIN"
    }
]

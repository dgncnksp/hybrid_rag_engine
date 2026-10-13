import re

class PIIMasker:
    """
    Kullanıcı sorgularındaki ve dokümanlardaki hassas verileri (PII)
    LLM veya dış servislere sızmaması için maskeleyen güvenlik bileşeni.
    """
    def __init__(self):
        # TCKN (11 haneli), E-posta, Telefon ve Kredi Kartı regex kalıpları
        self.patterns = {
            "TCKN": r'\b[1-9][0-9]{10}\b',
            "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "PHONE": r'\b(?:\+?90|0)?\s*[5][0-9]{2}\s*[0-9]{3}\s*[0-9]{2}\s*[0-9]{2}\b',
            "CREDIT_CARD": r'\b(?:\d[ -]*?){13,16}\b'
        }

    def mask(self, text: str) -> str:
        masked_text = text
        for pii_type, pattern in self.patterns.items():
            masked_text = re.sub(pattern, f"[{pii_type}_MASKED]", masked_text)
        return masked_text

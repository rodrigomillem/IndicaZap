# app/services/classificacao.py
import re
from typing import Optional

# Dicionário básico (pode crescer depois)
CATEGORIAS = {
    "pintor": ["pintor", "pintura", "pintando", "pintar"],
    "eletricista": ["eletricista", "elétrica", "chuveiro", "tomada", "disjuntor"],
    "diarista": ["diarista", "faxina", "limpeza", "faxineira"],
    "encanador": ["encanador", "vazamento", "cano", "hidráulica"],
}


# ============================================================
# 1) Classificação baseada APENAS no conteúdo do VCF
# ============================================================

def classificar_por_vcf(texto: str) -> Optional[str]:
    texto = texto.lower()

    for categoria, termos in CATEGORIAS.items():
        if any(t in texto for t in termos):
            return categoria

    return None


# ============================================================
# 2) Classificação baseada no contexto do chat (fallback)
# ============================================================

def classificar_por_contexto(contexto: str) -> Optional[str]:
    contexto = contexto.lower()

    for categoria, termos in CATEGORIAS.items():
        if any(t in contexto for t in termos):
            return categoria

    return None
# app/services/classificacao_avancada.py

import re
import numpy as np
from typing import Optional, Dict, List


# ============================================================
# DEFINIÇÃO DE CATEGORIAS E TERMOS RELACIONADOS
# ============================================================

CATEGORIAS = {
    "pintor": [
        "pintor", "pintura", "pintar", "pinturas residenciais",
        "pintor de parede", "pintura interna", "pintura externa"
    ],
    "eletricista": [
        "eletricista", "elétrica", "chuveiro", "tomada",
        "disjuntor", "curto", "fiação", "lâmpada"
    ],
    "diarista": [
        "diarista", "faxina", "limpeza", "faxineira",
        "pós-obra", "limpeza pesada"
    ],
    "encanador": [
        "encanador", "vazamento", "canos", "hidráulica",
        "ralo entupido", "chuveiro pingando"
    ],
    "marceneiro": [
        "marceneiro", "marcenaria", "móveis planejados",
        "madeira", "armário", "ripado"
    ],
    "chaveiro": [
        "chaveiro", "chaves", "troca de fechadura", "cadeado"
    ],
    "vidraceiro": [
        "vidraceiro", "vidro", "box", "espelho", "janelas de vidro"
    ],
}


# ============================================================
#  EMBEDDINGS — versão offline e simples
#  (pode ser substituído por modelos reais depois)
# ============================================================

def gerar_embedding(texto: str) -> np.ndarray:
    """
    Gerador de embeddings extremamente simples.
    Substitua por SentenceTransformer / OpenAI quando quiser.
    """
    texto = texto.lower()

    vetor = np.zeros(300)

    for i, ch in enumerate(texto.encode("utf-8")):
        vetor[i % 300] += ch / 255.0

    norma = np.linalg.norm(vetor)

    return vetor / norma if norma > 0 else vetor


def similaridade(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


# ============================================================
# 1) CLASSIFICAÇÃO POR REGRAS DIRETAS (rápido)
# ============================================================

def classificar_por_regras(texto: str) -> Optional[str]:
    texto = texto.lower()

    # Regras simples → alta precisão e baixo custo
    for categoria, termos in CATEGORIAS.items():
        for termo in termos:
            if termo in texto:
                return categoria

    return None


# ============================================================
# 2) CLASSIFICAÇÃO SEMÂNTICA COM EMBEDDINGS
# ============================================================

def classificar_por_semantica(texto: str) -> Optional[str]:
    emb_texto = gerar_embedding(texto)

    melhor_categoria = None
    melhor_score = 0.0

    for categoria, termos in CATEGORIAS.items():
        for termo in termos:
            score = similaridade(emb_texto, gerar_embedding(termo))

            if score > melhor_score:
                melhor_score = score
                melhor_categoria = categoria

    # threshold de confiança mínima
    if melhor_score < 0.45:
        return None

    return melhor_categoria


# ============================================================
# 3) FUNÇÃO FINAL — CLASSIFICAÇÃO INTELIGENTE COM MULTICAMADAS
# ============================================================

def classificar_inteligente(texto: str) -> Optional[str]:
    """
    Pipeline final:
    1. regras simples
    2. semântica via embeddings
    """

    if not texto:
        return None

    # 1) Regras diretas
    categoria = classificar_por_regras(texto)
    if categoria:
        return categoria

    # 2) Embeddings semânticos
    categoria = classificar_por_semantica(texto)
    if categoria:
        return categoria

    # 3) Sem categoria encontrada
    return None
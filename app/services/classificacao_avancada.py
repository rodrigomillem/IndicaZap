# app/services/classificacao_avancada.py

import numpy as np
from typing import Optional
from app.services.categorias_lista_grande import CATEGORIAS


def gerar_embedding(texto: str) -> np.ndarray:
    texto = texto.lower()
    vetor = np.zeros(300)
    for i, ch in enumerate(texto.encode("utf-8")):
        vetor[i % 300] += ch / 255.0
    norma = np.linalg.norm(vetor)
    return vetor / norma if norma > 0 else vetor


def similaridade(a: np.ndarray, b: np.ndarray) -> float:
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b))


def classificar_por_regras(texto: str) -> Optional[str]:
    texto = texto.lower()
    for categoria, termos in CATEGORIAS.items():
        for termo in termos:
            if termo in texto:
                return categoria
    return None


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

    return melhor_categoria if melhor_score >= 0.45 else None


def classificar_inteligente(texto: str) -> Optional[str]:
    if not texto:
        return None

    # 1. Regras diretas
    categoria = classificar_por_regras(texto)
    if categoria:
        return categoria

    # 2. Embeddings leves
    categoria = classificar_por_semantica(texto)
    if categoria:
        return categoria

    return None
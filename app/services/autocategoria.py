# app/services/autocategoria.py

import json
import numpy as np
from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import UUID

from app.services.classificacao_avancada import gerar_embedding
from app.services.categorias_lista_grande import CATEGORIAS
from app.database.models import CategoriaSugestao

LIMIAR_SIMILARIDADE = 0.65
LIMIAR_PROMOCAO = 3


def encontrar_categoria_existente(termo: str) -> bool:
    termo = termo.lower()
    for termos in CATEGORIAS.values():
        if termo in termos:
            return True
    return False


# ============================================================
#   ✔️ FUNÇÃO CORRIGIDA (VERSÃO FINAL COMPATÍVEL COM O E2E)
# ============================================================
def detectar_nova_categoria(texto: str) -> Optional[str]:
    import re

    texto = texto.lower()

    # Stopwords ampliadas para ignorar verbos/comuns
    stopwords = {
        "ele", "ela", "com", "de", "do", "da", "que", "um", "uma", "para", "e",
        "trabalha", "trabalhar", "faz", "fazer", "instala", "instalar",
        "mexer", "atua", "atuar", "tem", "possui"
    }

    # Extrair palavras válidas
    palavras = re.findall(r"[a-zA-Zà-ÿ]+", texto)

    # Todas as palavras já existentes nas categorias
    palavras_existentes = set()
    for termos in CATEGORIAS.values():
        for t in termos:
            for w in t.split():
                palavras_existentes.add(w.lower())

    # Retornar a primeira palavra nova realmente relevante
    for p in palavras:
        if len(p) < 4:
            continue
        if p in stopwords:
            continue
        if p not in palavras_existentes:
            return p

    return None


# ============================================================
#   Registro de sugestões
# ============================================================
def registrar_sugestao_categoria(db: Session, termo: str):
    termo = termo.lower()

    existente = (
        db.query(CategoriaSugestao)
        .filter(CategoriaSugestao.termo_base == termo)
        .first()
    )

    if existente:
        existente.count_ocorrencias += 1
        db.commit()
        return existente

    nova = CategoriaSugestao(
        termo_base=termo,
        termos_relacionados=json.dumps([]),
        count_ocorrencias=1
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


# ============================================================
#   Promoção de categorias após X ocorrências
# ============================================================
def promover_categorias(db: Session) -> List[str]:
    pendentes = (
        db.query(CategoriaSugestao)
        .filter(CategoriaSugestao.status == "pendente")
        .all()
    )

    promovidas = []

    for s in pendentes:
        if s.count_ocorrencias >= LIMIAR_PROMOCAO:
            CATEGORIAS[s.termo_base] = [s.termo_base]
            s.status = "aprovado"
            promovidas.append(s.termo_base)

    db.commit()
    return promovidas
# app/services/chat_pipeline.py

from typing import Dict
from uuid import UUID
from sqlalchemy.orm import Session

from app.services.classificacao_avancada import classificar_inteligente
from app.services.chat_busca_contexto import buscar_contexto_do_vcf, carregar_chat
from app.services.autocategoria import detectar_nova_categoria, registrar_sugestao_categoria, promover_categorias
from app.services import crud


CHAT_CACHE = {}


def registrar_chat(condominio_id: UUID, grupo_id: UUID, texto: str):
    CHAT_CACHE[(condominio_id, grupo_id)] = carregar_chat(texto)


def processar_profissionais_faltantes(db: Session, condominio_id: UUID, grupo_id: UUID) -> Dict:

    if (condominio_id, grupo_id) not in CHAT_CACHE:
        return {"erro": "Chat não enviado ainda"}

    linhas = CHAT_CACHE[(condominio_id, grupo_id)]
    profissionais = crud.list_profissionais(db)

    atualizados = []
    sugeridos = []

    for prof in profissionais:
        if prof.categoria:
            continue

        nome_vcf = prof.nome.lower().replace(" ", "") + ".vcf"
        contexto = buscar_contexto_do_vcf(linhas, nome_vcf)

        if not contexto:
            continue

        categoria = classificar_inteligente(contexto)

        if categoria:
            crud.update_profissional(db, prof.id, {"categoria": categoria})
            atualizados.append({"profissional": prof.nome, "categoria": categoria})
            continue

        # NÃO CLASSIFICOU → tentar aprender nova categoria
        nova = detectar_nova_categoria(contexto)
        if nova:
            registrar_sugestao_categoria(db, nova)
            sugeridos.append({"profissional": prof.nome, "categoria_sugerida": nova})

    promovidas = promover_categorias(db)

    return {
        "total_classificados": len(atualizados),
        "total_sugeridos": len(sugeridos),
        "novas_categorias_promovidas": promovidas,
        "classificados": atualizados,
        "sugeridos": sugeridos
    }
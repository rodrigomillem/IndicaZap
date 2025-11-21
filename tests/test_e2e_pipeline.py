# tests/test_e2e_pipeline.py

import uuid
import vobject
import pytest

from app.services.chat_pipeline import (
    registrar_chat,
    processar_profissionais_faltantes
)

from app.routers.vcf import extrair_vcf
from app.services.classificacao_avancada import classificar_inteligente
from app.services.autocategoria import (
    detectar_nova_categoria,
    registrar_sugestao_categoria,
    promover_categorias
)

from app.database.models import (
    Condominio,
    Profissional,
    CategoriaSugestao
)


@pytest.mark.integration
def test_pipeline_e2e_completo(db_session):
    """
    Teste E2E – fluxo completo:
    1. Upload VCF
    2. Classificação IA
    3. Registrar profissional
    4. Upload Chat
    5. Buscar contexto
    6. Classificação via contexto
    7. Descoberta automática de categoria se necessário
    8. Promoção de categoria
    """

    # ============================================================
    # 1. Criar condomínio (simulando o caso real)
    # ============================================================

    condominio = Condominio(
        id=uuid.uuid4(),
        nome="Condomínio Teste"
    )

    db_session.add(condominio)
    db_session.commit()


    # ============================================================
    # 2. Criar profissional via VCF (sem categoria)
    # ============================================================

    v = vobject.vCard()
    v.add("fn").value = "Carlos Instalador"
    v.add("tel").value = "(11) 90000-1111"
    v.add("note").value = "instala qualquer coisa"
    raw = v.serialize().encode("utf-8")

    nome, telefone, email, notas = extrair_vcf(raw)

    prof = Profissional(
        id=uuid.uuid4(),
        nome=nome,
        telefone=telefone,
        email=email,
        descricao_raw_vcf=notas,
        categoria=None   # não classificado ainda
    )

    db_session.add(prof)
    db_session.commit()


    # ============================================================
    # 3. Upload de Chat (simula conversa real)
    # ============================================================

    chat = """
        Tem o contato?
        carlosinstalador.vcf
        Ele instala split e faz manutenção de ar condicionado
    """

    registrar_chat(condominio.id, condominio.id, chat)


    # ============================================================
    # 4. Pipeline de classificação via chat
    # ============================================================

    resultado = processar_profissionais_faltantes(
        db_session,
        condominio.id,
        condominio.id
    )

    # Deve ter sido classificado como "ar-condicionado"
    assert resultado["total_classificados"] == 1
    assert resultado["classificados"][0]["categoria"] == "ar-condicionado"


    # ============================================================
    # 5. Testar AutoCategoria: termo desconhecido
    # ============================================================

    texto_novo = "ele trabalha com esquadrias de alumínio"

    nova = detectar_nova_categoria(texto_novo)
    assert nova == "esquadrias"

    registrar_sugestao_categoria(db_session, nova)
    registrar_sugestao_categoria(db_session, nova)
    registrar_sugestao_categoria(db_session, nova)

    promovidas = promover_categorias(db_session)

    assert "esquadrias" in promovidas

    # CategoriaSugestao no banco virou aprovado
    cat_db = (
        db_session.query(CategoriaSugestao)
        .filter(CategoriaSugestao.termo_base == "esquadrias")
        .first()
    )

    assert cat_db.status == "aprovado"
# tests/test_pipeline_chat.py

from app.services.chat_pipeline import processar_profissionais_faltantes, registrar_chat
from app.database.models import Profissional, Condominio
import uuid


def test_pipeline_chat_classifica_profissional(db_session):
    condominio = Condominio(id=uuid.uuid4(), nome="Teste")
    db_session.add(condominio)
    db_session.commit()

    # Profissional sem categoria
    prof = Profissional(
        id=uuid.uuid4(),
        nome="Joao Silva",
        telefone="11999998888",
        categoria=None
    )
    db_session.add(prof)
    db_session.commit()

    # Chat simulando envio do VCF
    chat_texto = """
        Alguém tem contato?
        joaosilva.vcf
        Ele arruma disjuntor e a parte elétrica
    """

    registrar_chat(condominio.id, condominio.id, chat_texto)

    result = processar_profissionais_faltantes(
        db_session,
        condominio.id,
        condominio.id
    )

    assert result["total_classificados"] == 1
    assert result["classificados"][0]["categoria"] == "eletricista"
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.database.models import (
    Condominio,
    Grupo,
    Mensagem,
    Recomendacao,
    Profissional
)

from app.schemas.schemas import (
    CondominioCreate,
    GrupoCreate,
    MensagemCreate,
    RecomendacaoCreate
)

from app.schemas.profissional import (
    ProfissionalCreate,
    ProfissionalUpdate
)

# ============================================================
#  CRUD: CONDOMÍNIOS
# ============================================================

def create_condominio(db: Session, data: CondominioCreate):
    condominio = Condominio(
        nome=data.nome,
        endereco=data.endereco,
        cidade=data.cidade,
        unidades=data.unidades,
        sindico=data.sindico,
        telefone=data.telefone,
        criado_em=datetime.utcnow()
    )
    db.add(condominio)
    db.commit()
    db.refresh(condominio)
    return condominio


def list_condominios(db: Session):
    return db.query(Condominio).all()


def get_condominio(db: Session, condominio_id: UUID):
    return db.query(Condominio).filter(Condominio.id == condominio_id).first()


# ============================================================
#  CRUD: GRUPOS
# ============================================================

def create_grupo(db: Session, data: GrupoCreate):
    grupo = Grupo(
        nome=data.nome,
        link=data.link,
        condominio_id=data.condominio_id,
        criado_em=datetime.utcnow()
    )
    db.add(grupo)
    db.commit()
    db.refresh(grupo)
    return grupo


def list_grupos(db: Session):
    return db.query(Grupo).all()


def list_grupos_por_condominio(db: Session, condominio_id: UUID):
    return db.query(Grupo).filter(Grupo.condominio_id == condominio_id).all()


def get_grupo(db: Session, grupo_id: UUID):
    return db.query(Grupo).filter(Grupo.id == grupo_id).first()


# ============================================================
#  CRUD: MENSAGENS
# ============================================================

def create_mensagem(db: Session, data: MensagemCreate):
    mensagem = Mensagem(
        grupo_id=data.grupo_id,
        conteudo=data.conteudo,
        criado_em=datetime.utcnow()
    )
    db.add(mensagem)
    db.commit()
    db.refresh(mensagem)
    return mensagem


def list_mensagens_por_grupo(db: Session, grupo_id: UUID):
    return db.query(Mensagem).filter(Mensagem.grupo_id == grupo_id).all()


# ============================================================
#  CRUD: RECOMENDAÇÕES
# ============================================================

def create_recomendacao(db: Session, data: RecomendacaoCreate):
    recomendacao = Recomendacao(
        grupo_id=data.grupo_id,
        recomendacao=data.recomendacao,
        criado_em=datetime.utcnow()
    )
    db.add(recomendacao)
    db.commit()
    db.refresh(recomendacao)
    return recomendacao


def list_recomendacoes_por_grupo(db: Session, grupo_id: UUID):
    return db.query(Recomendacao).filter(Recomendacao.grupo_id == grupo_id).all()


# ============================================================
#  CRUD: PROFISSIONAIS
# ============================================================

def create_or_update_profissional(db: Session, data: ProfissionalCreate):
    """
    Telefone é identificador único.
    Se existir → atualiza.
    Senão → cria.
    """

    existente = (
        db.query(Profissional)
        .filter(Profissional.telefone == data.telefone)
        .first()
    )

    if existente:
        if data.nome:
            existente.nome = data.nome
        if data.email:
            existente.email = data.email
        if data.descricao_raw_vcf:
            existente.descricao_raw_vcf = data.descricao_raw_vcf
        if data.categoria:
            existente.categoria = data.categoria

        db.commit()
        db.refresh(existente)
        return existente

    novo = Profissional(
        nome=data.nome,
        telefone=data.telefone,
        email=data.email,
        descricao_raw_vcf=data.descricao_raw_vcf,
        categoria=data.categoria,
        criado_em=datetime.utcnow()
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


def get_profissional(db: Session, profissional_id: UUID):
    return db.query(Profissional).filter(Profissional.id == profissional_id).first()


def list_profissionais(db: Session):
    return db.query(Profissional).order_by(Profissional.nome.asc()).all()


# ============================================================
#  CORREÇÃO IMPORTANTE AQUI
# ============================================================

def update_profissional(db: Session, profissional_id: UUID, data):
    """
    Aceita tanto:
    - ProfissionalUpdate (Pydantic)
    - dict com campos para atualização
    """

    profissional = get_profissional(db, profissional_id)

    if not profissional:
        return None

    # Caso o chamador envie um dict (como no pipeline E2E)
    if isinstance(data, dict):
        for key, value in data.items():
            setattr(profissional, key, value)

        db.commit()
        db.refresh(profissional)
        return profissional

    # Caso venha um ProfissionalUpdate (Pydantic)
    if data.nome is not None:
        profissional.nome = data.nome

    if data.telefone is not None:
        profissional.telefone = data.telefone

    if data.email is not None:
        profissional.email = data.email

    if data.descricao_raw_vcf is not None:
        profissional.descricao_raw_vcf = data.descricao_raw_vcf

    if data.categoria is not None:
        profissional.categoria = data.categoria

    db.commit()
    db.refresh(profissional)
    return profissional


def delete_profissional(db: Session, profissional_id: UUID):
    profissional = get_profissional(db, profissional_id)

    if not profissional:
        return False

    db.delete(profissional)
    db.commit()
    return True


# ============================================================
#  VÍNCULO PROFISSIONAL <-> CONDOMÍNIO (N:N)
# ============================================================

def vincular_profissional_condominio(db: Session, profissional_id: UUID, condominio_id: UUID):
    profissional = get_profissional(db, profissional_id)
    condominio = get_condominio(db, condominio_id)

    if not profissional or not condominio:
        return None

    if condominio not in profissional.condominios:
        profissional.condominios.append(condominio)
        db.commit()
        db.refresh(profissional)

    return profissional
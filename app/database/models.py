from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Integer,
    ForeignKey,
    Table
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.database import Base


# ============================================================
#  RELAÇÃO N:N — PROFISSIONAL <-> CONDOMÍNIO
# ============================================================

profissional_condominio = Table(
    "profissional_condominio",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("profissional_id", UUID(as_uuid=True), ForeignKey("profissionais.id")),
    Column("condominio_id", UUID(as_uuid=True), ForeignKey("condominios.id"))
)


# ============================================================
#  MODELO: CONDOMÍNIO
# ============================================================

class Condominio(Base):
    __tablename__ = "condominios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(255), nullable=False)
    endereco = Column(String(255), nullable=True)
    cidade = Column(String(100), nullable=True)
    unidades = Column(Integer, nullable=True)
    sindico = Column(String(255), nullable=True)
    telefone = Column(String(50), nullable=True)

    criado_em = Column(DateTime, default=datetime.utcnow)

    grupos = relationship("Grupo", back_populates="condominio")

    profissionais = relationship(
        "Profissional",
        secondary=profissional_condominio,
        back_populates="condominios"
    )


# ============================================================
#  MODELO: GRUPO
# ============================================================

class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(255), nullable=False)
    link = Column(String(255), nullable=True)

    condominio_id = Column(UUID(as_uuid=True), ForeignKey("condominios.id"))
    criado_em = Column(DateTime, default=datetime.utcnow)

    condominio = relationship("Condominio", back_populates="grupos")

    mensagens = relationship("Mensagem", back_populates="grupo")
    recomendacoes = relationship("Recomendacao", back_populates="grupo")


# ============================================================
#  MODELO: MENSAGEM (contexto do chat)
# ============================================================

class Mensagem(Base):
    __tablename__ = "mensagens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    grupo_id = Column(UUID(as_uuid=True), ForeignKey("grupos.id"))
    conteudo = Column(Text, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    grupo = relationship("Grupo", back_populates="mensagens")


# ============================================================
#  MODELO: RECOMENDAÇÃO
# ============================================================

class Recomendacao(Base):
    __tablename__ = "recomendacoes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    grupo_id = Column(UUID(as_uuid=True), ForeignKey("grupos.id"))
    recomendacao = Column(Text, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    grupo = relationship("Grupo", back_populates="recomendacoes")


# ============================================================
#  MODELO: PROFISSIONAL
# ============================================================

class Profissional(Base):
    __tablename__ = "profissionais"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    nome = Column(String(255), nullable=False)

    # Telefone é o identificador único
    telefone = Column(String(50), unique=True, nullable=False)

    email = Column(String(255), nullable=True)
    descricao_raw_vcf = Column(Text, nullable=True)

    # Categoria (classe) detectada por IA
    categoria = Column(String(100), nullable=True)

    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    condominios = relationship(
        "Condominio",
        secondary=profissional_condominio,
        back_populates="profissionais"
    )


# ============================================================
#  MODELO: CATEGORIAS SUGERIDAS (AutoCategory Discovery)
# ============================================================

class CategoriaSugestao(Base):
    __tablename__ = "categorias_sugeridas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    termo_base = Column(String(255), nullable=False)

    # JSON contendo termos relacionados
    termos_relacionados = Column(Text, nullable=True)

    count_ocorrencias = Column(Integer, default=1)

    # estados possíveis: pendente, aprovado, descartado
    status = Column(String(50), default="pendente")

    criado_em = Column(DateTime, default=datetime.utcnow)
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime


# ============================================================
#  SCHEMAS: CONDOMINIOS
# ============================================================

class CondominioBase(BaseModel):
    nome: str
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    unidades: Optional[int] = None
    sindico: Optional[str] = None
    telefone: Optional[str] = None


class CondominioCreate(CondominioBase):
    pass


class CondominioResponse(CondominioBase):
    id: UUID
    criado_em: datetime

    class Config:
        from_attributes = True  # importante no SQLAlchemy 2.0


# ============================================================
#  SCHEMAS: GRUPOS
# ============================================================

class GrupoBase(BaseModel):
    nome: str
    link: str
    condominio_id: Optional[UUID] = None


class GrupoCreate(GrupoBase):
    pass


class GrupoResponse(GrupoBase):
    id: UUID
    criado_em: datetime

    class Config:
        from_attributes = True


# ============================================================
#  SCHEMAS: MENSAGENS
# ============================================================

class MensagemBase(BaseModel):
    grupo_id: UUID
    conteudo: str


class MensagemCreate(MensagemBase):
    pass


class MensagemResponse(MensagemBase):
    id: UUID
    criado_em: datetime

    class Config:
        from_attributes = True


# ============================================================
#  SCHEMAS: RECOMENDACOES
# ============================================================

class RecomendacaoBase(BaseModel):
    grupo_id: UUID
    recomendacao: str


class RecomendacaoCreate(RecomendacaoBase):
    pass


class RecomendacaoResponse(RecomendacaoBase):
    id: UUID
    criado_em: datetime

    class Config:
        from_attributes = True
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List

from app.schemas.profissional import ProfissionalResponse


# ============================================
# Base
# ============================================

class CondominioBase(BaseModel):
    nome: str
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    unidades: Optional[int] = None
    sindico: Optional[str] = None
    telefone: Optional[str] = None


# ============================================
# Create
# ============================================

class CondominioCreate(CondominioBase):
    pass


# ============================================
# Update
# ============================================

class CondominioUpdate(BaseModel):
    nome: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    unidades: Optional[int] = None
    sindico: Optional[str] = None
    telefone: Optional[str] = None


# ============================================
# Response simples (sem profissionais)
# ============================================

class CondominioResponse(CondominioBase):
    id: UUID
    criado_em: datetime

    class Config:
        orm_mode = True


# ============================================
# Response completo com profissionais
# ============================================

class CondominioCompletoResponse(CondominioResponse):
    profissionais: List[ProfissionalResponse] = []
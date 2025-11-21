from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List


# ============================================
# Base
# ============================================

class ProfissionalBase(BaseModel):
    nome: str
    telefone: str
    email: Optional[str] = None
    descricao_raw_vcf: Optional[str] = None
    categoria: Optional[str] = None


# ============================================
# Create
# ============================================

class ProfissionalCreate(ProfissionalBase):
    pass


# ============================================
# Update
# ============================================

class ProfissionalUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    descricao_raw_vcf: Optional[str] = None
    categoria: Optional[str] = None


# ============================================
# Response
# ============================================

class ProfissionalResponse(ProfissionalBase):
    id: UUID
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        orm_mode = True
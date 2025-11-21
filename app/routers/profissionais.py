from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.database import get_db
from app.schemas.profissional import (
    ProfissionalCreate,
    ProfissionalUpdate,
    ProfissionalResponse
)
from app.services import crud


router = APIRouter(
    prefix="/profissionais",
    tags=["Profissionais"]
)


# ============================================================
#  Criar ou atualizar profissional (telefone é único)
# ============================================================

@router.post("/", response_model=ProfissionalResponse)
def criar_ou_atualizar_profissional(
    data: ProfissionalCreate,
    db: Session = Depends(get_db)
):
    profissional = crud.create_or_update_profissional(db, data)
    return profissional


# ============================================================
#  Listar profissionais
# ============================================================

@router.get("/", response_model=list[ProfissionalResponse])
def listar_profissionais(db: Session = Depends(get_db)):
    return crud.list_profissionais(db)


# ============================================================
#  Buscar profissional por ID
# ============================================================

@router.get("/{profissional_id}", response_model=ProfissionalResponse)
def buscar_profissional(
    profissional_id: UUID,
    db: Session = Depends(get_db)
):
    profissional = crud.get_profissional(db, profissional_id)

    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    return profissional


# ============================================================
#  Atualizar profissional
# ============================================================

@router.put("/{profissional_id}", response_model=ProfissionalResponse)
def atualizar_profissional(
    profissional_id: UUID,
    data: ProfissionalUpdate,
    db: Session = Depends(get_db)
):
    profissional = crud.update_profissional(db, profissional_id, data)

    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    return profissional


# ============================================================
#  Deletar profissional
# ============================================================

@router.delete("/{profissional_id}")
def deletar_profissional(
    profissional_id: UUID,
    db: Session = Depends(get_db)
):
    sucesso = crud.delete_profissional(db, profissional_id)

    if not sucesso:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    return {"detail": "Profissional deletado com sucesso"}


# ============================================================
#  Vincular profissional ↔ condomínio (N:N)
# ============================================================

@router.post("/{profissional_id}/condominios/{condominio_id}", response_model=ProfissionalResponse)
def vincular_profissional_a_condominio(
    profissional_id: UUID,
    condominio_id: UUID,
    db: Session = Depends(get_db)
):
    profissional = crud.vincular_profissional_condominio(db, profissional_id, condominio_id)

    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional ou condomínio não encontrado")

    return profissional
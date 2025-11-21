from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.database import get_db
from app.schemas.schemas import GrupoCreate, GrupoResponse
from app.services import crud

router = APIRouter(prefix="/grupos", tags=["Grupos"])


@router.post("/", response_model=GrupoResponse)
def criar_grupo(data: GrupoCreate, db: Session = Depends(get_db)):
    return crud.create_grupo(db, data)


@router.get("/", response_model=list[GrupoResponse])
def listar_grupos(db: Session = Depends(get_db)):
    return crud.list_grupos(db)


@router.get("/condominio/{condominio_id}", response_model=list[GrupoResponse])
def listar_grupos_por_condominio(condominio_id: UUID, db: Session = Depends(get_db)):
    return crud.list_grupos_por_condominio(db, condominio_id)


@router.get("/{grupo_id}", response_model=GrupoResponse)
def obter_grupo(grupo_id: UUID, db: Session = Depends(get_db)):
    return crud.get_grupo(db, grupo_id)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.database import get_db
from app.schemas.schemas import CondominioCreate, CondominioResponse
from app.services import crud

router = APIRouter(prefix="/condominios", tags=["Condomínios"])


@router.post("/", response_model=CondominioResponse)
def criar_condominio(data: CondominioCreate, db: Session = Depends(get_db)):
    return crud.create_condominio(db, data)


@router.get("/", response_model=list[CondominioResponse])
def listar_condominios(db: Session = Depends(get_db)):
    return crud.list_condominios(db)


@router.get("/{condominio_id}", response_model=CondominioResponse)
def obter_condominio(condominio_id: UUID, db: Session = Depends(get_db)):
    return crud.get_condominio(db, condominio_id)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.database import get_db
from app.schemas.schemas import MensagemCreate, MensagemResponse
from app.services import crud

router = APIRouter(prefix="/mensagens", tags=["Mensagens"])


@router.post("/", response_model=MensagemResponse)
def criar_mensagem(data: MensagemCreate, db: Session = Depends(get_db)):
    return crud.create_mensagem(db, data)


@router.get("/grupo/{grupo_id}", response_model=list[MensagemResponse])
def listar_mensagens_por_grupo(grupo_id: UUID, db: Session = Depends(get_db)):
    return crud.list_mensagens_por_grupo(db, grupo_id)
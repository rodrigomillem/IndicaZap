from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.database import get_db
from app.schemas.schemas import RecomendacaoCreate, RecomendacaoResponse
from app.services import crud

router = APIRouter(prefix="/recomendacoes", tags=["Recomendações"])


@router.post("/", response_model=RecomendacaoResponse)
def criar_recomendacao(data: RecomendacaoCreate, db: Session = Depends(get_db)):
    return crud.create_recomendacao(db, data)


@router.get("/grupo/{grupo_id}", response_model=list[RecomendacaoResponse])
def listar_recomendacoes_por_grupo(grupo_id: UUID, db: Session = Depends(get_db)):
    return crud.list_recomendacoes_por_grupo(db, grupo_id)
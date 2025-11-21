from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import CategoriaSugestao
from app.services.autocategoria import promover_categorias

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get("/sugeridas")
def listar_sugeridas(db: Session = Depends(get_db)):
    return db.query(CategoriaSugestao).filter(CategoriaSugestao.status == "pendente").all()


@router.post("/promover")
def promover(db: Session = Depends(get_db)):
    novas = promover_categorias(db)
    return {"novas_categorias": novas}
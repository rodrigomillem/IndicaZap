# app/routers/chat.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.database import get_db
from app.services.chat_pipeline import registrar_chat, processar_profissionais_faltantes

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/upload/{condominio_id}/{grupo_id}")
async def upload_chat(
    condominio_id: UUID,
    grupo_id: UUID,
    arquivo: UploadFile = File(...)
):
    if not arquivo.filename.lower().endswith(".txt"):
        raise HTTPException(400, "O arquivo deve ser .txt")

    texto = (await arquivo.read()).decode("utf-8")

    registrar_chat(condominio_id, grupo_id, texto)

    return {"status": "chat armazenado"}


@router.post("/classificar-faltantes/{condominio_id}/{grupo_id}")
def classificar_faltantes(
    condominio_id: UUID,
    grupo_id: UUID,
    db: Session = Depends(get_db)
):
    return processar_profissionais_faltantes(db, condominio_id, grupo_id)
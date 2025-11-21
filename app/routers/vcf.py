# app/routers/vcf.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import vobject
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.database import get_db
from app.schemas.profissional import ProfissionalCreate, ProfissionalResponse
from app.services import crud
from app.services.classificacao_avancada import classificar_inteligente


router = APIRouter(prefix="/vcf", tags=["VCF"])


def extrair_vcf(conteudo: bytes):
    v = vobject.readOne(conteudo.decode("utf-8"))
    nome = v.fn.value if hasattr(v, "fn") else "Sem nome"

    telefone = None
    if hasattr(v, "tel"):
        telefone = (
            v.tel.value.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        )

    notas = v.note.value if hasattr(v, "note") else ""
    email = v.email.value if hasattr(v, "email") else None

    return nome, telefone, email, notas


@router.post("/upload/{condominio_id}", response_model=ProfissionalResponse)
async def upload_vcf(condominio_id: UUID, arquivo: UploadFile = File(...), db: Session = Depends(get_db)):

    if not arquivo.filename.lower().endswith(".vcf"):
        raise HTTPException(400, "Arquivo deve ser .vcf")

    nome, telefone, email, notas = extrair_vcf(await arquivo.read())

    if not telefone:
        raise HTTPException(400, "Telefone não encontrado no VCF")

    categoria = classificar_inteligente(f"{nome} {notas}")

    profissional = crud.create_or_update_profissional(
        db,
        ProfissionalCreate(
            nome=nome,
            telefone=telefone,
            email=email,
            descricao_raw_vcf=notas,
            categoria=categoria
        )
    )

    crud.vincular_profissional_condominio(db, profissional.id, condominio_id)

    return profissional
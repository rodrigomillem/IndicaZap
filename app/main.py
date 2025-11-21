from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import engine
from app.database.models import Base

# Importação das rotas existentes
from app.routers import (
    condominios,
    grupos,
    mensagens,
    recomendacoes,
    profissionais,
    vcf
)

# ================================================
# Inicializa a API
# ================================================
app = FastAPI(
    title="IndicaZap API",
    description=(
        "Backend do sistema IndicaZap — gestão de condomínios, grupos, "
        "profissionais indicados e processamento de arquivos .vcf."
    ),
    version="1.0.1"
)

# ================================================
# Habilita CORS (importante para frontend futuro)
# ================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # liberação total (ajuste depois se quiser)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================================
# Registrar Rotas
# ================================================
app.include_router(condominios.router)
app.include_router(grupos.router)
app.include_router(mensagens.router)
app.include_router(recomendacoes.router)

# Novas rotas adicionadas
app.include_router(profissionais.router)
app.include_router(vcf.router)

# ================================================
# Cria as tabelas automaticamente (se não existirem)
# ================================================
Base.metadata.create_all(bind=engine)

# ================================================
# Rota base (teste)
# ================================================
@app.get("/")
def root():
    return {
        "status": "OK",
        "message": "IndicaZap API está online com suporte a profissionais e upload de VCF!"
    }
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Nova base declarativa (SQLAlchemy 2.0+)
class Base(DeclarativeBase):
    pass

# Cria o engine de conexão com o Supabase
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Mantém conexões vivas no Pooler do Supabase
)

# Fabricação de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependência padrão para FastAPI (se usar)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("🔌 Testando conexão com Supabase...")

try:
    # Cria engine do SQLAlchemy
    engine = create_engine(DATABASE_URL)

    # Abre conexão
    with engine.connect() as conn:
        # Executa comando SQL usando text()
        result = conn.execute(text("SELECT NOW();"))
        row = result.fetchone()

        print("✅ Conectado com sucesso!")
        print("Hora no servidor:", row[0])

except Exception as e:
    print("❌ Erro ao conectar:")
    print(e)
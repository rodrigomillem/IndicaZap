from sqlalchemy import Column, Integer, String
from app.database import Base


class Condominium(Base):
    __tablename__ = "condominiums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
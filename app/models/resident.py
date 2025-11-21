from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Resident(Base):
    __tablename__ = "residents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    condominium_id = Column(Integer, ForeignKey("condominiums.id"), nullable=False)
    condominium = relationship("Condominium", backref="residents")
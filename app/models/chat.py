from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    condominium_id = Column(Integer, ForeignKey("condominiums.id"))
    condominium = relationship("Condominium", backref="chats")
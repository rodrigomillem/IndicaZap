from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base


class Mention(Base):
    __tablename__ = "mentions"

    id = Column(Integer, primary_key=True, index=True)

    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    professional_id = Column(Integer, ForeignKey("professionals.id"), nullable=False)
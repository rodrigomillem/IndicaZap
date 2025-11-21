from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)

    professional_id = Column(Integer, ForeignKey("professionals.id"), nullable=False)
    score = Column(Integer, nullable=False)
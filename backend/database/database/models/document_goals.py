from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, ARRAY
from sqlalchemy.orm import relationship
from database.database import Base


class DocumentGoal(Base):
    __tablename__ = "document_goals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    is_reached = Column(Boolean, default=False, nullable=False)
    document = relationship("Document", back_populates="document_goals")

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from db.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False, server_default="")
    was_created = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="documents")
    validations = relationship("Validation", back_populates="document")

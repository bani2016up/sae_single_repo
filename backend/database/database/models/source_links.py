from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, ARRAY
from sqlalchemy.orm import relationship
from database.database import Base


class SourceLink(Base):
    __tablename__ = "source_links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    href = Column(String, nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    document = relationship("Document", back_populates="source_links")

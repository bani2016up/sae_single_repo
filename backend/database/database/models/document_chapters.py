from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, ARRAY
from sqlalchemy.orm import relationship
from database.database import Base




class DocumentChapter(Base):
    __tablename__ = "document_chapters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    document = relationship("Document", back_populates="document_chapters")
    sections = relationship("DocumentSection", back_populates="document_chapter")

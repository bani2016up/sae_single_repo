from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, ARRAY
from sqlalchemy.orm import relationship
from database.database import Base


class DocumentSection(Base):
    __tablename__ = "document_sections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    chapter_id = Column(Integer, ForeignKey("document_chapters.id"), nullable=False)
    document_chapter = relationship("DocumentChapter", back_populates="sections")

from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, ARRAY
from sqlalchemy.orm import relationship
from database.database import Base


class ProjectSection(Base):
    __tablename__ = "project_sections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    chapter_id = Column(Integer, ForeignKey("project_chapters.id"), nullable=False)

from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, ARRAY
from sqlalchemy.orm import relationship
from database.database import Base




class ProjectChapter(Base):
    __tablename__ = "project_chapters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

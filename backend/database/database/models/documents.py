from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, ARRAY
from sqlalchemy.orm import relationship
from database.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    sub_title = Column(String, nullable=True)
    abstract = Column(String, nullable=True)
    keywords = Column(ARRAY(String), nullable=True)  # List of keywords
    study_organization = Column(String, nullable=True)
    user = relationship("User", back_populates="documents")
    document_goals = relationship("DocumentGoal", back_populates="document")
    source_links = relationship("SourceLink", back_populates="document")
    document_chapters = relationship("DocumentChapter", back_populates="document")

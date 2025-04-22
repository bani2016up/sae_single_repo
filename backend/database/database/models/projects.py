from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, ARRAY
from sqlalchemy.orm import relationship
from database.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    sub_title = Column(String, nullable=True)
    abstract = Column(String, nullable=True)
    keywords = Column(ARRAY(String), nullable=True)  # List of keywords
    study_organization = Column(String, nullable=True)

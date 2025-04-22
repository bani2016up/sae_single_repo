from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, ARRAY
from sqlalchemy.orm import relationship
from database.database import Base


class ProjectGoal(Base):
    __tablename__ = "project_goals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    is_reached = Column(Boolean, default=False, nullable=False)

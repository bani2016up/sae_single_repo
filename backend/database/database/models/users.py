from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, ARRAY
from sqlalchemy.orm import relationship
from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)  # Simplified description field
    sub_title = Column(String, nullable=True)
    abstract = Column(String, nullable=True)
    keywords = Column(ARRAY(String), nullable=True)  # List of keywords
    study_organization = Column(String, nullable=True)


class UserToProject(Base):
    __tablename__ = "user_to_project"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    role = Column(String, nullable=False)  # Role in the project
    permissions = Column(String, nullable=True)  # Permissions in the project
    last_modified = Column(DateTime(timezone=True), nullable=True)
    last_viewed = Column(DateTime(timezone=True), nullable=False)


class ProjectGoal(Base):
    __tablename__ = "project_goals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    is_reached = Column(Boolean, default=False, nullable=False)


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    content = Column(Text, nullable=True)  # Document content
    last_modified = Column(DateTime(timezone=True), nullable=False)


class SourceLink(Base):
    __tablename__ = "source_links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    href = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)


class ProjectChapter(Base):
    __tablename__ = "project_chapters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)


class ProjectSection(Base):
    __tablename__ = "project_sections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    chapter_id = Column(Integer, ForeignKey("project_chapters.id"), nullable=False)

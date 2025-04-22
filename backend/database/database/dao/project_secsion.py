from models.users import ProjectSection
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from database.dao import TemplateDAO, construct_dao


_project_section_dao = construct_dao(ProjectSection)

class _Project_SectionDAO(_project_section_dao):
    ...


UserDAO = _Project_SectionDAO(ProjectSection)

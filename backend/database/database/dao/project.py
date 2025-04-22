from models.users import Project
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from database.dao import TemplateDAO, construct_dao


_project_dao = construct_dao(Project)

class _ProjectDAO(_project_dao):
    ...


UserDAO = _ProjectDAO(Project)

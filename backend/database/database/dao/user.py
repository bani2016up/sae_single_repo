from models.users import User
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from database.dao import TemplateDAO, construct_dao


_user_dao = construct_dao(User)

class _UserDAO(_user_dao):
    ...


UserDAO = _UserDAO(User)

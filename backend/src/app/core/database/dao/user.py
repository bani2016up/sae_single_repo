from ..models.users import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy import Result, ScalarResult

from ..db.dao import TemplateDAO, construct_dao


_user_dao = construct_dao(User)

class _UserDAO(_user_dao):
    ...


UserDAO = _UserDAO(User)

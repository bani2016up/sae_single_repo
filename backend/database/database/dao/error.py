from ..models.errors import Error
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy import Result, ScalarResult

from ..database.dao import TemplateDAO, construct_dao


_error_dao = construct_dao(Error)

class _ErrorDAO(_error_dao):
    ...


ErrorDAO = _ErrorDAO(Error)

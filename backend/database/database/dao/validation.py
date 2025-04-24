from models.validations import Validation
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy import Result, ScalarResult

from database.dao import TemplateDAO, construct_dao


_validation_dao = construct_dao(Validation)

class _ValidationDAO(_validation_dao):
    ...


ValidationDAO = _ValidationDAO(Validation)

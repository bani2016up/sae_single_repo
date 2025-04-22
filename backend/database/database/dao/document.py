from models.users import Document
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from database.dao import TemplateDAO, construct_dao


_document_dao = construct_dao(Document)

class _DocumentDAO(_document_dao):
    ...


DocumentDAO = _DocumentDAO(Document)

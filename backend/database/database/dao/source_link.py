from models.source_links import SourceLink
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from database.dao import TemplateDAO, construct_dao


_source_link_dao = construct_dao(SourceLink)

class _Source_LinkDAO(_source_link_dao):
    ...


Source_LinkDAO = _Source_LinkDAO(SourceLink)

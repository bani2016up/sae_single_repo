from models.document_sections import DocumentSection
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from db.dao import TemplateDAO, construct_dao


_document_section_dao = construct_dao(DocumentSection)

class _Document_SectionDAO(_document_section_dao):
    ...


Document_SectionDAO = _Document_SectionDAO(DocumentSection)

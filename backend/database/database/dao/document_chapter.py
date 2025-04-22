from models.users import DocumentChapter
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from database.dao import TemplateDAO, construct_dao


_document_chapter_dao = construct_dao(DocumentChapter)

class _Document_ChapterDAO(_document_chapter_dao):
    ...


Project_ChapterDAO = _Document_ChapterDAO(DocumentChapter)

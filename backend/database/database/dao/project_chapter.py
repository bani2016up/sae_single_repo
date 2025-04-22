from models.users import ProjectChapter
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from database.dao import TemplateDAO, construct_dao


_project_chapter_dao = construct_dao(ProjectChapter)

class _Project_ChapterDAO(_project_chapter_dao):
    ...


Project_ChapterDAO = _Project_ChapterDAO(ProjectChapter)

from models.users import DocumentGoal
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from database.dao import TemplateDAO, construct_dao


_document_goal_dao = construct_dao(DocumentGoal)

class _Document_GoalDAO(_document_goal_dao):
    ...


Document_GoalDAO = _Document_GoalDAO(DocumentGoal)

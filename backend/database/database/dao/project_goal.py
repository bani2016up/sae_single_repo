from models.users import ProjectGoal
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from database.dao import TemplateDAO, construct_dao


_project_goal_dao = construct_dao(ProjectGoal)

class _Project_GoalDAO(_project_goal_dao):
    ...


UserDAO = _Project_GoalDAO(ProjectGoal)

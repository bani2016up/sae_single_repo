from ..models.users import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy import Result, ScalarResult

from ..db.dao import TemplateDAO, construct_dao


_user_dao = construct_dao(User)

class _UserDAO(_user_dao):

    @staticmethod
    async def get_by_external_id(external_id: str, sess: AsyncSession) -> User | None:
        return (await sess.execute(select(User).where(User.external_id == external_id))).scalar_one_or_none()


UserDAO = _UserDAO(User)

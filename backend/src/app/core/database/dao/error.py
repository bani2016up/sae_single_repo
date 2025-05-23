from ..models.errors import Error
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy import Result, ScalarResult

from ..db.dao import TemplateDAO, construct_dao


_error_dao = construct_dao(Error)

class _ErrorDAO(_error_dao):

    @staticmethod
    async def delete_where_validation_id(validation_id: int, sess: AsyncSession) -> None:
        """
        Deletes all errors associated with a given validation ID.

        :param validation_id: The ID of the validation whose errors are to be deleted.
        :param sess: The AsyncSession instance.
        """
        stmt = delete(Error).where(Error.validation_id == validation_id)
        await sess.execute(stmt)


ErrorDAO = _ErrorDAO(Error)

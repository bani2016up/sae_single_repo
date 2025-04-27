from ..models.validations import Validation
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy import Result, ScalarResult
from typing import Optional

from ..db.dao import TemplateDAO, construct_dao


_validation_dao = construct_dao(Validation)

class _ValidationDAO(_validation_dao):
    async def get_validation_by_document_id(self, document_id: int, sess: AsyncSession) -> Optional[Validation]:
        """
        Returns a single validation for a given document ID.

        :param document_id: The ID of the document whose validation is to be fetched.
        :param sess: The AsyncSession instance.
        :return: A Validation object if found, otherwise None.
        """
        stmt = select(Validation).where(Validation.document_id == document_id)
        result = await sess.execute(stmt)
        return result.scalar_one_or_none()


ValidationDAO = _ValidationDAO(Validation)

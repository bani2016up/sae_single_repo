from models.documents import Document
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy import Result, ScalarResult

from database.dao import TemplateDAO, construct_dao


_document_dao = construct_dao(Document)

class _DocumentDAO(_document_dao):
    async def get_documents_by_user_id(self, user_id: int, sess: AsyncSession) -> ScalarResult[Document]:
        """
        Returns a list of document parameters for a given user ID.

        :param user_id: The ID of the user whose documents are to be fetched.
        :param sess: The AsyncSession instance.
        :return: A list of dictionaries containing document parameters.
        """
        stmt = select(Document).where(Document.user_id == user_id)
        result = await sess.execute(stmt)
        return result.scalars().all()


DocumentDAO = _DocumentDAO(Document)

from .database import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Type, TypeVar, Generic

from sqlalchemy import select, delete, update


T = TypeVar("T", bound=Base)


class TemplateDAO(Generic[T]):
    def __init__(self, db_model: T) -> None:
        self.db_model: T = db_model

    async def get(self, id: int, sess: AsyncSession) -> T | None:
        stmt = select(self.db_model).where(self.db_model.id == id)
        return (await sess.execute(stmt)).scalar_one_or_none()

    async def get_scalar(self, id: int, sess: AsyncSession) -> T:
        stmt = select(self.db_model).where(self.db_model.id == id)
        return (await sess.execute(stmt)).scalar_one()

    async def delete(self, id: int, sess: AsyncSession) -> None:
        stmt = self.db_model.__table__.delete().where(self.db_model.id == id)
        await sess.execute(stmt)

    async def update(self, id: int, values: dict, sess: AsyncSession) -> T:
        stmt = (
            self.db_model.__table__.update()
            .where(self.db_model.id == id)
            .values(**values)
        )
        await sess.execute(stmt)
        return await self.get_scalar(id, sess)

    async def create(self, instance: T, sess: AsyncSession) -> T:
        sess.add(instance)
        await sess.flush()
        return instance

    async def create_all(self, instances: list[T], sess: AsyncSession) -> list[T]:
        sess.add_all(instances)
        await sess.flush()
        return instances


def construct_dao(db_model: Type[T]) -> Type[TemplateDAO[T]]:
    class CustomDAO(TemplateDAO[T]):
        def __init__(self, db_model: T) -> None:
            super(CustomDAO, self).__init__(db_model)

    return CustomDAO

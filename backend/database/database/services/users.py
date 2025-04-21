from models.users import User
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users.request import UserUpdate, UserCreate
from dao.user import UserDAO



async def create_user(data: UserCreate, sess: AsyncSession) -> User:
    user = User(
        username=data.username,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        )
    return await UserDAO.create(user, sess)


async def get_user(id: int, sess: AsyncSession) -> User | None:
    return await UserDAO.get(id, sess)


async def update_user(data: UserUpdate, id: int, sess: AsyncSession) -> User | None:
    user = await UserDAO.get(id, sess)
    if not user:
        return None
    update_data = data.dict(exclude_unset=True)
    return await UserDAO.update(id, update_data, sess)


async def delete_user(id: int, sess: AsyncSession) -> bool:
    user = await UserDAO.get(id, sess)
    if not user:
        return False
    await UserDAO.delete(id, sess)
    return True

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import SessionLocal
from services.users import create_user, get_user, update_user, delete_user
from schemas.users.request import UserCreate, UserUpdate


async def main():
    try:
        # Initialize the database session
        async with SessionLocal() as session:
            # Example: Create a new user
            user_data = UserCreate(
                username="johndoe",
                first_name="John",
                last_name="Doe",
                email="johndoe@example.com",
            )
            new_user = await create_user(user_data, session)
            print(f"Created User: {new_user}")

            # Example: Get the created user by ID
            user = await get_user(new_user.id, session)
            print(f"Retrieved User: {user}")

            # Example: Update the user's information
            update_data = UserUpdate(
                first_name="Jonathan",
                last_name="Smith",
                email="jonathansmith@example.com"
            )
            updated_user = await update_user(update_data, new_user.id, session)
            print(f"Updated User: {updated_user}")

            # Example: Delete the user
            is_deleted = await delete_user(new_user.id, session)
            print(f"User Deleted: {is_deleted}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())

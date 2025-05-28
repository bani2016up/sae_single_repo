from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
import os

# Import your Base and models
from app.core.database.models import User, Document, Validation, Error, Base
# Import all your models here

# Load environment variables from .env
load_dotenv()

# Get the async DATABASE_URL from the .env file
ASYNC_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
if not ASYNC_DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the .env file")

# Convert the async DATABASE_URL to a sync one for Alembic
SYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("asyncpg", "psycopg2")

# Alembic Config object, which provides access to the .ini file values
config = context.config

# Set the sqlalchemy.url dynamically from the SYNC_DATABASE_URL
config.set_main_option("sqlalchemy.url", SYNC_DATABASE_URL)

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

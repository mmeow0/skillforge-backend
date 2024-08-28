from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.infrastructure.database import SQLALCHEMY_DATABASE_URL, Base

config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Set the target_metadata to the MetaData object from your Base
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=SQLALCHEMY_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        url=SQLALCHEMY_DATABASE_URL,
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

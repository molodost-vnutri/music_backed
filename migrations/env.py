from logging.config import fileConfig

from os.path import abspath, dirname
import sys

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from source.settings import settings
from source.database import Base
from source.users.models import UserModel, UserRoles, RoleModel
from source.music.models import MusicGenreModel, MusicModel, GenreModel, MusicEndModel

config = context.config

config.set_main_option("sqlalchemy.url", f"{settings.postgres_url}?async_fallback=True")

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
import os
import sys

# Ensure `calender_agent/` (parent of alembic/) is on sys.path so
# `from app.db...` works regardless of the cwd alembic is run from
# (repo root with `-c calender_agent/alembic.ini` or `calender_agent/` itself).
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Load DATABASE_URL from .env so alembic works without manual `export`.
# .env lives at the repo root; also check calender_agent/ and cwd.
try:
    from dotenv import load_dotenv

    _here = os.path.dirname(__file__)  # calender_agent/alembic
    _project_dir = os.path.dirname(_here)  # calender_agent
    _repo_root = os.path.dirname(_project_dir)  # repo root
    for _env_path in (
        os.path.join(os.getcwd(), ".env"),
        os.path.join(_project_dir, ".env"),
        os.path.join(_repo_root, ".env"),
    ):
        if os.path.isfile(_env_path):
            load_dotenv(_env_path, override=False)
except ImportError:
    pass

from app.db.database import Base
from app.db.models import Event

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

config = context.config

database_url = (os.getenv("DATABASE_URL") or "").strip().strip('"').strip("'")
if not database_url:
    raise RuntimeError(
        "DATABASE_URL is not set. Define it in .env or export it before "
        "running alembic."
    )

config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata



def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
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

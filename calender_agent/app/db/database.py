import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , DeclarativeBase

try:
    from dotenv import load_dotenv

    _here = os.path.dirname(__file__)  # calender_agent/app/db
    _project_dir = os.path.dirname(os.path.dirname(_here))  # calender_agent
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

DATABASE_URL = (os.getenv("DATABASE_URL") or "").strip().strip('"').strip("'")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Define it in .env or export it before "
        "running the app/alembic."
    )

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass
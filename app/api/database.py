import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("__DATABASE_URL__")

if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL no está definida en el archivo .env")

# URL de la base de la aplicación
db_url = make_url(DATABASE_URL)

# URL de la base postgres (para crear la BD)
postgres_url = db_url.set(database="postgres")

admin_engine = create_engine(
    postgres_url,
    isolation_level="AUTOCOMMIT",
)

with admin_engine.connect() as conn:

    exists = conn.execute(
        text(
            "SELECT 1 FROM pg_database WHERE datname = :dbname"
        ),
        {"dbname": db_url.database},
    ).scalar()

    if not exists:
        conn.execute(
            text(f'CREATE DATABASE "{db_url.database}"')
        )

admin_engine.dispose()

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_USER = "postgres"
DATABASE_PORT = "5432"
DATABASE_PASSWORD = "17051603"
DATABASE_HOST = "localhost"
DATABASE_NAME = "MS2"

DATABASE_URL = (
    f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}"
    f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def verify_table_exist(name: str) -> str | None:
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    if name in existing_tables:
        return name
    return None


def create_table(name: str):
    import models

    if verify_table_exist(name):
        print(f"Tabela {name} ja existe")
        return

    try:
        Base.metadata.create_all(bind=engine, tables=[Base.metadata.tables[name]])
    except KeyError:
        print(f"Erro: tabela {name} nao esta registrada nos models!")
        return

    if verify_table_exist(name):
        print(f"Tabela {name} criada com sucesso!")
    else:
        print(f"Houve um erro ao criar a tabela {name}!")

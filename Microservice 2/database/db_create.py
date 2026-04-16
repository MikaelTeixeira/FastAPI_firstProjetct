import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_database():
    usuario = "postgres"
    senha = "17051603"
    host = "localhost"
    porta = 5432
    nome_banco = "MS2"

    conn = psycopg2.connect(
        dbname="postgres",
        user=usuario,
        password=senha,
        host=host,
        port=porta,
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (nome_banco,))
    exists = cur.fetchone()

    if exists:
        print(f"Banco {nome_banco} ja existe")
    else:
        cur.execute(f"CREATE DATABASE {nome_banco}")
        print(f"Banco {nome_banco} criado com sucesso!")

    cur.close()
    conn.close()

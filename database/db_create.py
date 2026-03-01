import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



def create_database():
    usuario = "postgres"
    senha  = "17051603"
    host = "localhost"
    porta = 5432
    nome_banco = "prova6p"

    conn = psycopg2.connect(
        dbname = "postgres",
        user = usuario,
        password = senha,
        host = host,
        port = porta
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()

    cur.execute(f"CREATE DATABASE {nome_banco}")

    cur.close()
    conn.close()

    print(f"Banco {nome_banco} criado com sucesso!")
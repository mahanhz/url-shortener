import os

import psycopg


def get_connection():
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    username = os.getenv("DB_USERNAME", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    database = os.getenv("DB_NAME", "postgres")
    print(
        f"host={host} dbname={database} user={username} password={password} port={port}"
    )
    return psycopg.connect(
        f"host={host} dbname={database} user={username} password={password} port={port}"
    )


def create_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE urls (
        id SERIAL NOT NULL, 
        short_url_code VARCHAR NOT NULL, 
        original_url VARCHAR NOT NULL, 
        creation_time TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
        created_by VARCHAR, 
        expiration_time TIMESTAMP WITHOUT TIME ZONE, 
        PRIMARY KEY (id)
)
                """)
            conn.commit()


def delete_all_urls():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM urls")
            conn.commit()


def create_a_shortened_url(short_code: str, orig_url: str):
    query = "INSERT INTO urls (short_url_code, original_url, creation_time, created_by, expiration_time) VALUES (%s, %s, current_timestamp, 'me@example.com', current_timestamp)"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (short_code, orig_url))
            conn.commit()

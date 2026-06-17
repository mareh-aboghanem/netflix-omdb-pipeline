"""Storage functions for Postgres and Blob Storage."""

import json
import logging
import os
from contextlib import closing
from datetime import datetime, timezone
import pandas as pd
import psycopg2
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient

log = logging.getLogger(__name__)


def insert_readings(df: pd.DataFrame) -> None:
    db_url = os.environ["POSTGRES_URL"]
    schema = os.environ.get("DB_SCHEMA", "public")

    with closing(psycopg2.connect(db_url)) as conn:
        with conn.cursor() as cur:
            cur.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')  # noqa: S608
            cur.execute(f'SET search_path TO "{schema}"')  # noqa: S608
            # cur.execute("DROP TABLE IF EXISTS omdb_movies")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS omdb_movies (
                    imdb_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    year BIGINT NOT NULL,
                    released DATE,
                    imdb_score REAL,
                    imdb_votes BIGINT,
                    metascore BIGINT,
                    rottentomatoes BIGINT
                )
            """)

            for _, row in df.iterrows():
                query = """
                    INSERT INTO omdb_movies (imdb_id, title, year, released, imdb_score, imdb_votes, metascore, rottentomatoes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (imdb_id) DO NOTHING
                """
                cur.execute(
                    query,
                    (
                        row["imdb_id"],
                        row["title"],
                        int(row["year"]) if pd.notnull(row["year"]) else 0,
                        row["released"] if pd.notnull(row["released"]) else None,
                        (
                            float(row["imdb_score"])
                            if pd.notnull(row["imdb_score"])
                            else None
                        ),
                        (
                            int(row["imdb_votes"])
                            if pd.notnull(row["imdb_votes"])
                            else None
                        ),
                        int(row["metascore"]) if pd.notnull(row["metascore"]) else None,
                        (
                            int(row["rottentomatoes"])
                            if pd.notnull(row["rottentomatoes"])
                            else None
                        ),
                    ),
                )

        conn.commit()

    log.info("Inserted %d rows into %s.weather_readings", len(df), schema)


def upload_raw_json(raw_data) -> None:
    """Upload raw API response to Blob Storage as a JSON backup."""
    conn_str = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    client = BlobServiceClient.from_connection_string(conn_str)
    container = client.get_container_client("raw")
    try:
        container.create_container()
    except ResourceExistsError:
        pass

    blob_name = (
        f"pipeline/{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H%M%S')}.json"
    )
    container.upload_blob(
        name=blob_name,
        data=json.dumps(raw_data).encode("utf-8"),
        overwrite=True,
    )
    log.info("Uploaded raw data to blob: %s", blob_name)

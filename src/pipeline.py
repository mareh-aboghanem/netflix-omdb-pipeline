"""Main pipeline: fetch, validate, store."""

import logging
import requests
import os
import sys
from dotenv import load_dotenv
import pandas as pd
import time
from pydantic import ValidationError
from src.models import MovieDetails
from src.storage import insert_readings, upload_raw_json

load_dotenv()
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(message)s",
)
logging.getLogger("azure").setLevel(logging.WARNING)
log = logging.getLogger(__name__)


def fetch_data() -> list[dict]:
    """Fetch movie details from OMDb API using titles from the cleaned CSV."""
    OMDB_KEY = os.getenv("OMDB_API_KEY")
    BASE_URL = "http://www.omdbapi.com/"
    if not OMDB_KEY:
        logging.info("Error: OMDB_API_KEY is missing from environment variables.")
        return []
    csv_path = "./data/netflix_titles_cleaned.csv"
    if not os.path.exists(csv_path):
        log.warning(f"Error:Cleaned csv {csv_path} not found.")
        return []
    df = pd.read_csv(csv_path)
    titles_to_fetch = df["title"].head(5).tolist()
    raw_records = []
    delay = 1.0
    for title in titles_to_fetch:
        log.info(f"Fetching OMDb data for: {title}")
        try:
            response = requests.get(
                BASE_URL, params={"apikey": OMDB_KEY, "t": title}, timeout=10
            )
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 5))
                log.info(f"Rate limited, waiting {retry_after}s...")
                time.sleep(retry_after)
                response = requests.get(
                    BASE_URL, params={"apikey": OMDB_KEY, "t": title}, timeout=10
                )
            response.raise_for_status()
            data = response.json()

            if data.get("Response") == "True":
                raw_records.append(data)
            else:
                log.warning(f"Skipping: '{title}' not found on OMDb.")

        except requests.exceptions.RequestException as e:
            log.error(f"API Network Error for '{title}': {e}")
        time.sleep(delay)
    return raw_records


def validate(raw_records: list[dict]) -> tuple[list[MovieDetails], list[dict]]:
    """Validate raw records using Pydantic models, returning valid items."""
    valid = []
    for i, record in enumerate(raw_records):
        try:
            reading = MovieDetails(**record)
            valid.append(reading)
        except ValidationError as e:
            log.warning("Skipping invalid record at index %d: %s", i, e)

    log.info("Validated %d / %d records successfully.", len(valid), len(raw_records))
    return valid


def extract_rotten_tomatoes(rating_list: list):
    """This is a helper function it extract the Rotten Tomatoes value from Ratings coulmn"""
    if not isinstance(rating_list, list):
        return None
    for rating in rating_list:
        if rating.get("Source") == "Rotten Tomatoes":
            raw_value = rating.get("Value", "")
            return raw_value.replace("%", "").strip()
    return None


def transform(readings: list[MovieDetails], df_csv: pd.DataFrame) -> pd.DataFrame:
    """Transform API data, transform CSV data, and combine them together."""
    df_api = pd.DataFrame([r.model_dump() for r in readings])
    df_api["Year"] = pd.to_numeric(df_api["Year"], errors="coerce")
    df_api["Released"] = pd.to_datetime(df_api["Released"], errors="coerce")
    df_api["Runtime"] = df_api["Runtime"].str.replace(" min", "")
    df_api["Runtime"] = pd.to_numeric(df_api["Runtime"], errors="coerce")
    df_api["imdbRating"] = pd.to_numeric(df_api["imdbRating"], errors="coerce")
    df_api["Metascore"] = pd.to_numeric(df_api["Metascore"], errors="coerce")
    df_api["imdbVotes"] = df_api["imdbVotes"].str.replace(",", "")
    df_api["imdbVotes"] = pd.to_numeric(df_api["imdbVotes"], errors="coerce")
    text_columns = [
        "Rated",
        "Genre",
        "Language",
        "Country",
        "Awards",
        "DVD",
        "BoxOffice",
        "Production",
        "Website",
    ]
    df_api[text_columns] = df_api[text_columns].replace("N/A", None)
    df_api["Rotten Tomatoes"] = df_api["Ratings"].apply(extract_rotten_tomatoes)
    df_api["Rotten Tomatoes"] = pd.to_numeric(
        df_api["Rotten Tomatoes"], errors="coerce"
    )
    df_api = df_api.drop(columns=["Ratings"])
    df_api.columns = df_api.columns.str.lower()
    df_api["title_lower"] = df_api["title"].str.lower().str.strip()
    df_csv["title_lower"] = df_csv["title"].str.lower().str.strip()
    df_combined = pd.merge(df_api, df_csv, on="title_lower", suffixes=("_api", "_csv"))
    df_combined["title"] = df_combined["title_api"]
    df_final = pd.DataFrame()
    df_final["imdb_id"] = df_combined["imdbid"]
    df_final["title"] = df_combined["title"]
    df_final["year"] = df_combined["year"]
    df_final["released"] = df_combined["released"]
    df_final["imdb_score"] = df_combined["imdbrating"]
    df_final["imdb_votes"] = df_combined["imdbvotes"]
    df_final["metascore"] = df_combined["metascore"]
    df_final["rottentomatoes"] = df_combined["rotten tomatoes"]

    log.info("Successfully transformed and combined %d rows.", len(df_final))
    return df_final


def run():
    """Run the full pipeline: fetch -> validate -> transform -> store."""
    log.info("Pipeline starting")

    raw = fetch_data()
    if not raw:
        log.error("No raw data fetched from API.")
        sys.exit(1)
    readings = validate(raw)
    if not readings:
        log.error("No valid records to store")
        sys.exit(1)
    csv_path = "./data/netflix_titles_cleaned.csv"
    df_csv = pd.read_csv(csv_path)
    df = transform(readings, df_csv)
    df.to_csv("./data/combined_output_test.csv", index=False, encoding="utf-8")
    log.info("Saved a local copy of combined data to data/combined_output_test.csv")
    insert_readings(df)
    upload_raw_json(raw)

    log.info("Pipeline finished: %d records stored", len(df))


if __name__ == "__main__":
    # Fail fast if required env vars are missing
    for var in ["POSTGRES_URL", "AZURE_STORAGE_CONNECTION_STRING"]:
        if var not in os.environ:
            log.error("Missing required environment variable: %s", var)
            sys.exit(1)

    run()

import requests
import os
from dotenv import load_dotenv
import csv
import logging
import json

logging.basicConfig(level=logging.INFO, format="%(message)s")
load_dotenv()
OMDB_KEY = os.getenv("OMDB_API_KEY")
BASE_URL = "http://www.omdbapi.com/"
logger = logging.getLogger(__name__)


def fetch_movie_details(title):
    if not OMDB_KEY:
        logging.info("Error: OMDB_API_KEY is missing from environment variables.")
        return None

    try:
        response = requests.get(
            BASE_URL,
            params={"apikey": OMDB_KEY, "t": title},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "True":
            return data
        else:
            logging.info(f"Skipping: '{title}' not found on OMDb.")
            return None

    except requests.exceptions.RequestException as e:
        logger.warning(f"API Network Error for '{title}': {e}")
        return None


def process_netflix_data():
    csv_path = "./data/netflix_titles_cleaned.csv"
    if not os.path.exists(csv_path):
        logger.warning(f"Error: {csv_path} not found. Clean your CSV first!")
        return
    logging.info("Reading Cleaned Netflix CSV data...")
    with open(csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i >= 1:
                break

            title = row["title"]
            logging.info(f"\nFetching OMDb data for: {title}")
            omdb_data = fetch_movie_details(title)

            if omdb_data:
                """here i just want to check if the Rating column is repating the same values in MetaScore and imdbRating"""
                imdb_outer = omdb_data.get("imdbRating")
                meta_outer = omdb_data.get("Metascore")
                imdb_inner = None
                meta_inner = None
                ratings_list = omdb_data.get("Ratings", [])

                for rating in ratings_list:
                    if rating.get("Source") == "Internet Movie Database":
                        imdb_inner = rating.get("Value", "").split("/")[0]
                    elif rating.get("Source") == "Metacritic":
                        meta_inner = rating.get("Value", "").split("/")[0]
                logger.info(f"--- Verification for: {title} ---")
                logger.info(
                    f"Outer IMDb: {imdb_outer} | Inner IMDb: {imdb_inner} -> Match: {imdb_outer == imdb_inner}"
                )
                logger.info(
                    f"Outer Meta: {meta_outer} | Inner Meta: {meta_inner} -> Match: {meta_outer == meta_inner}"
                )
                """Fetching Data from OMDb Api"""
                logger.info("--------------------------------")
                pretty_json = json.dumps(omdb_data, indent=4)
                logger.info("Exact Raw JSON Response from OMDb:")
                logger.info(pretty_json)


if __name__ == "__main__":
    process_netflix_data()

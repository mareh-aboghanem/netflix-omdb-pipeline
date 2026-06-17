import os
import logging
from pathlib import Path
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
load_dotenv()


def download_kaggle_dataset():
    path_to_save = Path("./data")
    path_to_save.mkdir(parents=True, exist_ok=True)
    logger.info("Starting download for Netflix shows dataset...")
    username = os.getenv("KAGGLE_USERNAME")
    key = os.getenv("KAGGLE_API_TOKEN")
    if not username or not key:
        logger.error("Missing KAGGLE_USERNAME or KAGGLE_API_TOKEN in .env file!")
        return
    os.environ["KAGGLE_USERNAME"] = username
    os.environ["KAGGLE_KEY"] = key

    try:
        import subprocess

        command = "kaggle datasets download -d shivamb/netflix-shows -p ./data --unzip"
        subprocess.run(command, shell=True, check=True)
        logger.info("Download and extraction completed successfully!")
    except Exception as e:
        logger.error(f"An error occurred during download: {e}")


if __name__ == "__main__":
    download_kaggle_dataset()

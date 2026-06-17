import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
load_dotenv()
os.environ["KAGGLE_USERNAME"] = os.getenv("KAGGLE_USERNAME", "")
os.environ["KAGGLE_API_TOKEN"] = os.getenv("KAGGLE_API_TOKEN", "")



def download_kaggle_dataset():
    api = KaggleApi()
    api.authenticate()

    dataset = "shivamb/netflix-shows"
    path_to_save = Path("./data")
    path_to_save.mkdir(parents=True, exist_ok=True)
    logger.info(f"Starting download: {dataset} into {path_to_save}")
    api.dataset_download_files(dataset, path=str(path_to_save), unzip=True)
    logger.info("Download and extraction complete successfully!")


if __name__ == "__main__":
    download_kaggle_dataset()

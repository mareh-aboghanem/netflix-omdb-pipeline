import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def read_csv_data(data_path):
    try:
        df = pd.read_csv(data_path)
        logger.info(f"Successfully read data from {data_path}")
        return df
    except FileNotFoundError:
        logger.warning(f"Error: {data_path} not found")
        return None


def explore_csv_data(data_csv: pd.DataFrame):
    # data_csv=read_csv_data("./netflix_titles.csv")
    if data_csv is not None:
        logger.info("--- Exploring Data ---")
        logger.info("CSV Structure:")
        data_csv.info()
        logger.info("------------------------------")
        logger.info(f"\nDescribe:\n{data_csv.describe()}")
        logger.info("------------------------------")
        logger.info(f"\nFirst 5 rows:\n{data_csv.head(10)}")
        logger.info("------------------------------")
        logger.info(f"\nMissing Values:\n{data_csv.isna().sum()}")
        logger.info("------------------------------")
        logger.info(f"Columns: {data_csv.columns.tolist()}")
        logger.info("------------------------------")
        logger.info(f"Data Types:\n{data_csv.dtypes}")
        logger.info("------------------------------")
        logger.info(f"Duplicate Rows:\n{data_csv.duplicated().sum()}")
        return data_csv

    else:
        logger.warning("No DataFrame to analyze.")
        return None


"""the data_cleaning_file.md explain why i chose to clean the data like this."""


def clean_csv_data(data_csv: pd.DataFrame):
    if data_csv is not None:
        cleaned_df = data_csv.copy()
        logger.info("--- Cleaning Data ---")
        cleaned_df.fillna(
            {"director": "Unknown", "cast": "Unknown", "country": "Unknown"},
            inplace=True,
        )
        logger.info("Filled missing values for 'director', 'cast', and 'country'.")
        cleaned_df["date_added"] = pd.to_datetime(
            cleaned_df["date_added"], errors="coerce"
        )
        logger.info("Converted 'date_added' to datetime.")
        cleaned_df.dropna(subset=["date_added", "rating", "duration"], inplace=True)
        logger.info("Removed missing values.")
        cleaned_df.reset_index(drop=True, inplace=True)
        logger.info("Reset index after cleaning.")

        return cleaned_df
    else:
        logger.warning("No DataFrame to clean.")
        return None


if __name__ == "__main__":
    df = read_csv_data("./data/netflix_titles.csv")
    explore_csv_data(df)
    df_cleaned = clean_csv_data(df)
    if df_cleaned is not None:
        output_path = "./data/netflix_titles_cleaned.csv"
        df_cleaned.to_csv(output_path, index=False)
        logger.info(f"Cleaned data saved to {output_path}")
        explore_csv_data(df_cleaned)

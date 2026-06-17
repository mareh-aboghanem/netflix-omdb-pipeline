# Data Discovery & Cleaning Report

### 📊 Discovery Netflix_titles.csv
* **Scale:** 8,807 rows, 12 columns.
* **Types:** `release_year` is a number (`int64`), all others are text (`str`).

### 🔍 Issues & Strategy
1. **Big Gaps:** `director` (2,634), `country` (831), `cast` (825).
   * *Strategy:* I fill with 'Unknown' to save the data.
2. **Small Gaps:** `date_added` (10), `rating` (4), `duration` (3).
   * *Strategy:* I drop these rows.

### 🛠️ Cleaning Pipeline
1. **Copy:** I cloned the data to protect the original file.
2. **Impute:** I filled missing `director`, `cast`, and `country` with `"Unknown"`.
3. **Format:** I converted `date_added` to datetime.
4. **Drop:** I removed the remaining few rows with nulls.
5. **Reset:** I re-arranged row numbers from 0.

### 🏆 Final Metrics
* **Final Rows:** **8,702** (105 rows removed).
* **Missing Values:** Exactly **0**.
* **Duplicates:** **0**.

### 💾 Output
Saved at: `./data/netflix_titles_cleaned.csv`

### 📊 Discovery OMDb API & Integration
* **Data Source:** Live data from OMDb API using Netflix IMDb IDs.
* **Scale:** Tested with 5 movie records.
* **Types:** Mixed data (Texts, Numbers, and a list for Ratings).

### 🔍 Issues & Strategy
1. **Nested Ratings:** The API returns ratings inside a complex list.
   * *Strategy:* Extracted `Rotten Tomatoes` and `Metascore` into separate, clean columns.
2. **Missing Values:** Some fields from the API were completely empty (e.g., *Blood & Water*).
   * *Strategy:* Used Python to replace empty values with `None` so the database accepts them.
3. **Integer Overflow:** Big numbers (like *Kota Factory* with 86,711 votes) caused the database to crash.
   * *Strategy:* Changed the database column types from `INTEGER` to `BIGINT` to handle large numbers safely.

### 🛠️ Enriched Cleaning Pipeline
1. **Fetch:** Collected data safely from the OMDb API.
2. **Validate:** Used Pydantic (`MovieDetails`) to check data quality.
3. **Transform:** Cleaned commas from votes and flattened the ratings list using Pandas.
4. **Load:** Saved raw JSON to Azure Blob Storage and clean rows to Postgres (`omdb_movies`).

### 🏆 Final Enriched Metrics
* **Total Rows:** **5** rows successfully enriched.
* **Table Name:** `omdb_movies`
* **Status:** **100% Success** (No errors, all empty fields handled perfectly).
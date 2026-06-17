# AI Assistance Log

Document every time you used an AI tool during this project: what you asked, what it gave you, and what you changed before using it.

This is not about proving you worked hard. It is about building the habit of treating AI output as a first draft, not a final answer.

## Tools used

<!--I used only Gemini -->

-

## Log

<!-- One entry per significant AI interaction. Add as many as you need. -->

### Entry 1

**What I asked:** <!-- Traceback (most recent call last):

File "<frozen runpy>", line 198, in \_run_module_as_main
File "<frozen runpy>", line 88, in \_run_code
File "/app/src/pipeline.py", line 166, in <module>
run()
File "/app/src/pipeline.py", line 153, in run
insert_readings(df)
File "/app/src/storage.py", line 39, in insert_readings
cur.execute()
psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "omdb_movies_pkey"

DETAIL: Key (imdb_id)=(tt11394180) already exists.

((vweek7) )

when i run the run command for docker i got this why -->

**What it gave me:** <!-- 🔍 Cause of the Error
Primary Key Constraint: The imdb_id column in the Postgres database is configured as a Primary Key, which strictly prohibits duplicate entries.

The Root Cause: When the pipeline was re-run, it attempted to execute a standard INSERT for a movie (e.g., Dick Johnson Is Dead) that had already been saved during a previous execution. Postgres blocked the operation to maintain data integrity, triggering a UniqueViolation error.

🛠️ Resolution Strategy
The UPSERT Approach: The solution requires shifting from a blind INSERT to an UPSERT (Update or Insert) strategy.

Actionable Step: Modify the SQL query inside the insert_readings function within src/storage.py by appending an ON CONFLICT clause -->

**What I changed:** <!--I didn't use UPSERT because I thought it was safe to do ON CONFLICT (imdb_id) DO NOTHING. I'm not sure of my choice, but I think it's better than overwriting data.-->

---

### Entry 2

**What I asked:** <!--{"TimeStamp":"2026-06-17T19:23:52.4090408+00:00","Log":"updated and saved netflix_titles_cleaned.csv!"}
{"TimeStamp":"2026-06-17T19:23:52.4090666+00:00","Log":"OMDB_API_KEY is missing from environment variables."}
{"TimeStamp":"2026-06-17T19:23:52.4090793+00:00","Log":"raw data fetched from API."}

should i write my key?-->

**What it gave me:**<!--The AI confirmed that the data-cleaning cycle succeeded, but the cloud API enrichment stage was skipped because the server lacked an access token. It suggested using az containerapp job update --set-env-vars OMDB_API_KEY=YOUR_KEY to update the job configuration.-->

**What I changed:** <!--After the AI explained that it is safe because of `--set-env-vars`, I ran the command to inject my real API key directly into Azure's secure store.-->

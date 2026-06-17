FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
#RUN uv sync --frozen --no-dev
RUN uv sync --frozen

COPY src/ ./src/
COPY data/ ./data/
COPY tests/ ./tests/

COPY fetch_kaggle_data.py fetch_OMDb_api.py conftest.py ./

CMD ["uv", "run", "python", "-m", "src.pipeline"]
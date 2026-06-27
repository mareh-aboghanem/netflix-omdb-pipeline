"""Pydantic models for data validation."""

from pydantic import BaseModel, ConfigDict


class RatingItem(BaseModel):
    """Sub-model for the nested ratings list from OMDb."""

    Source: str
    Value: str


class MovieDetails(BaseModel):
    """Pydantic model to validate incoming data from OMDb API."""

    model_config = ConfigDict(populate_by_name=True)

    Title: str
    Year: str
    Rated: str | None = "N/A"
    Released: str | None = "N/A"
    Runtime: str | None = "N/A"
    Genre: str | None = "N/A"
    Director: str | None = "Unknown"
    Writer: str | None = "Unknown"
    Actors: str | None = "Unknown"
    Plot: str | None = None
    Language: str | None = "N/A"
    Country: str | None = "N/A"
    Awards: str | None = "N/A"
    Poster: str | None = None
    Ratings: list[RatingItem] | None = []
    Metascore: str | None = "N/A"
    imdbRating: str | None = "N/A"
    imdbVotes: str | None = "N/A"
    imdbID: str
    Type: str | None = "movie"
    DVD: str | None = "N/A"
    BoxOffice: str | None = "N/A"
    Production: str | None = "N/A"
    Website: str | None = "N/A"
    Response: str
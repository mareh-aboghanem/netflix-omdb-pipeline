"""Pydantic models for data validation. Replace with your own."""

from pydantic import BaseModel
from typing import Optional, List


class RatingItem(BaseModel):
    """Sub-model for the nested ratings list from OMDb."""

    Source: str
    Value: str


class MovieDetails(BaseModel):
    """Pydantic model to validate incoming data from OMDb API."""

    Title: str
    Year: str
    Rated: Optional[str] = "N/A"
    Released: Optional[str] = "N/A"
    Runtime: Optional[str] = "N/A"
    Genre: Optional[str] = "N/A"
    Director: Optional[str] = "Unknown"
    Writer: Optional[str] = "Unknown"
    Actors: Optional[str] = "Unknown"
    Plot: Optional[str] = None
    Language: Optional[str] = "N/A"
    Country: Optional[str] = "N/A"
    Awards: Optional[str] = "N/A"
    Poster: Optional[str] = None
    Ratings: Optional[List[RatingItem]] = []
    Metascore: Optional[str] = "N/A"
    imdbRating: Optional[str] = "N/A"
    imdbVotes: Optional[str] = "N/A"
    imdbID: str
    Type: Optional[str] = "movie"
    DVD: Optional[str] = "N/A"
    BoxOffice: Optional[str] = "N/A"
    Production: Optional[str] = "N/A"
    Website: Optional[str] = "N/A"
    Response: str

    class Config:
        """Pydantic configuration."""

        populate_by_name = True

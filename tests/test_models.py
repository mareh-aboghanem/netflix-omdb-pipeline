"""Tests for MovieDetails Pydantic models."""

import pytest
from pydantic import ValidationError
from src.models import MovieDetails


def test_valid_movie_reading():
    """A valid record should be accepted."""
    reading = MovieDetails(
        Title="Copenhagen",
        Year="2026",
        imdbID="tt11394180",
        Response="True",
    )
    assert reading.Title == "Copenhagen"
    assert reading.Year == "2026"
    assert reading.imdbID == "tt11394180"


def test_missing_required_field():
    """Missing required fields like 'Response' should raise a ValidationError."""
    with pytest.raises(ValidationError):
        MovieDetails(Title="Copenhagen", Year="2026")


def test_valid_ratings_list():
    """A movie with a properly structured ratings list should be accepted."""
    reading = MovieDetails(
        Title="Copenhagen",
        Year="2026",
        imdbID="tt11394180",
        Response="True",
        Ratings=[{"Source": "Rotten Tomatoes", "Value": "99%"}],
    )
    assert len(reading.Ratings) == 1
    assert reading.Ratings[0].Source == "Rotten Tomatoes"
    assert reading.Ratings[0].Value == "99%"

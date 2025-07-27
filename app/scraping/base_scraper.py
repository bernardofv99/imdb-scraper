from abc import ABC, abstractmethod
from typing import List, Dict

from app.schemas.movie import MovieIn

class BaseMovieScraper(ABC):
    @abstractmethod
    def get_top_movies(self, limit: int = 50) -> List[Dict]:
        pass

    def validate_movie_data(self, movie: dict) -> bool:
        """
        Validate if the movie data contains all required fields.
        """
        required_fields = [
            name
            for name, field in MovieIn.model_fields.items()
            if field.is_required()
        ]

        for field in required_fields:
            if field not in movie or movie[field] is None:
                return False
        return True
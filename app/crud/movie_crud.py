from app.db.session import SessionLocal
from app.models.movie import Movie
from app.models.actor import Actor
from app.schemas.movie import MovieIn

import logging
logger = logging.getLogger(__name__)


def insert_movie_if_not_exists(movie_data: dict) -> bool:
    session = SessionLocal()
    try:
        movie_in = MovieIn.model_validate(movie_data)

        # Validate movie data
        existing = session.query(Movie).filter_by(external_id=movie_in.external_id).first()
        if existing:
            logger.warning(f"Movie {movie_in.title} already exists.")
            return False

        # Create a new Movie instance
        movie = Movie(**movie_in.model_dump(exclude={"actors"}, mode="json"))
        session.add(movie)
        session.flush()

        # Add actors if they exist in the data
        for actor_name in movie_data.get("actors", []):
            actor = session.query(Actor).filter_by(name=actor_name).first()
            if not actor:
                actor = Actor(name=actor_name)
                session.add(actor)
                session.flush()

            movie.actors.append(actor)

        session.commit()
        logger.info(f"Inserted movie: {movie.title} with {len(movie.actors)} actors.")
        return True

    except Exception as e:
        session.rollback()
        logger.error(f"Error inserting movie {movie_data.get('title')}: {e}")
        return False
    finally:
        session.close()

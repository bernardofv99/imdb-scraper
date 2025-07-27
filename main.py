from app.utils.logging_config import setup_logging
setup_logging()

from app.scraping.imdb_scraper import IMDbScraper
from app.crud.movie_crud import insert_movie_if_not_exists
from app.utils.export_csv import export_to_csv
from app.db.session import SessionLocal
from app.models.movie import Movie

import logging
logger = logging.getLogger(__name__)


def run_scraper():
    logger.info("=== Starting IMDb Scraper ===")
    scraper = IMDbScraper()

    logger.info("Fetching movies...")
    movies = scraper.get_top_movies(limit=50)
    logger.info(f"Fetched {len(movies)} valid movies.")

    if not movies:
        logger.warning("No valid movies were scraped. Skipping database insertion and CSV export.")
        return

    logger.info("Inserting movies into database...")
    inserted_count = 0
    for movie in movies:
        if insert_movie_if_not_exists(movie):
            inserted_count += 1

    logger.info(f"Movies inserted: {inserted_count} / {len(movies)}")

    logger.info("Exporting movies to CSV from database...")
    session = SessionLocal()
    try:
        all_movies = session.query(Movie).all()
        export_to_csv(all_movies)
    finally:
        session.close()

    logger.info("=== Scraper Finished ===")


if __name__ == "__main__":
    run_scraper()

from datetime import datetime
from pathlib import Path
import csv

import logging
logger = logging.getLogger(__name__)

def export_to_csv(movies: list, filename: str = None):
    if not movies:
        logger.warning("No movies to export. Skipping CSV creation.")
        return

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_movies_{timestamp}.csv"

    output_path = Path("exports")
    output_path.mkdir(exist_ok=True)
    file_path = output_path / filename

    logger.info(f"Writing {len(movies)} movies to {file_path}...")

    fieldnames = [
        "title", "rating", "year", "duration_minutes", "metascore",
        "actors", "detail_url", "external_id", "platform"
    ]

    with open(file_path, mode="w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for movie in movies:
            writer.writerow({
                "title": movie.title,
                "rating": movie.rating,
                "year": movie.year,
                "duration_minutes": movie.duration_minutes,
                "metascore": movie.metascore,
                "actors": ", ".join(actor.name for actor in movie.actors),
                "detail_url": str(movie.detail_url),
                "external_id": movie.external_id,
                "platform": movie.platform.value,
            })

    logger.info(f"CSV export completed: {file_path}")

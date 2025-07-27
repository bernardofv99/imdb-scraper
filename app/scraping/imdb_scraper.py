import requests
from bs4 import BeautifulSoup
import json
from app.models.movie import PlatformEnum
from app.scraping.base_scraper import BaseMovieScraper

import logging
logger = logging.getLogger(__name__)


IMDB_TOP_URL = "https://www.imdb.com/chart/top/"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

class IMDbScraper(BaseMovieScraper):
    def get_top_movies(self, limit: int = 50):
        logger.info(f"Scraping top {limit} IMDb movies...")

        try:
            response = requests.get(IMDB_TOP_URL, headers=HEADERS)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to fetch IMDb page: {e}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        next_data_script = soup.find("script", id="__NEXT_DATA__")

        if not next_data_script:
            logger.error("No <script id='__NEXT_DATA__'> found in IMDb HTML.")
            return []

        try:
            raw_json = json.loads(next_data_script.string)
            edges = raw_json["props"]["pageProps"]["pageData"]["chartTitles"]["edges"]
        except Exception as e:
            logger.error(f"Failed to parse IMDb JSON data: {e}")
            return []

        movies = []
        for i, edge in enumerate(edges[:limit], start=1):
            try:
                node = edge["node"]
                imdb_id = node["id"]
                title = node["originalTitleText"]["text"]

                logger.debug(f"Parsing movie #{i}: {title} ({imdb_id})")

                movie = {
                    "title": title,
                    "rating": float(node["ratingsSummary"].get("aggregateRating", 0)),
                    "year": node["releaseYear"]["year"],
                    "duration_minutes": int(node.get("runtime", {}).get("seconds", 0) / 60) if node.get("runtime") else None,
                    "detail_url": f"https://www.imdb.com/title/{imdb_id}/",
                    "platform": PlatformEnum.IMDB,
                    "external_id": imdb_id,
                }

                movie.update(self._parse_movie_details(movie["detail_url"]))

                if self.validate_movie_data(movie):
                    movies.append(movie)
                else:
                    logger.warning(f"Skipping movie with missing required data: {title}")

            except Exception as e:
                logger.error(f"Error parsing movie #{i}: {e}")

        logger.info(f"Scraping complete. Valid movies collected: {len(movies)}")
        return movies

    def _parse_movie_details(self, detail_url: str) -> dict:
        try:
            response = requests.get(detail_url, headers=HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # --- Obtener Metascore ---
            metascore = None
            meta_tag = soup.select_one("span.metacritic-score-box")
            if meta_tag:
                try:
                    metascore = int(meta_tag.text.strip())
                except ValueError:
                    pass

            # --- Obtener actores principales ---
            cast_tags = soup.select('[data-testid="title-cast-item__actor"]')
            actors = [tag.text.strip() for tag in cast_tags[:3]]

            return {
                "metascore": metascore,
                "actors": actors
            }

        except Exception as e:
            logger.warning(f"Failed to parse movie details from {detail_url}: {e}")
            return {
                "metascore": None,
                "actors": []
            }

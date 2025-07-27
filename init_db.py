import logging
from app.db.session import Base, engine
from app.models.movie import Movie
from app.models.actor import Actor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    logger.info("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)

    logger.info("Creating all tables...")
    Base.metadata.create_all(bind=engine)

    logger.info("[!] Tables created successfully.")

if __name__ == "__main__":
    init_db()

from sqlalchemy import Column, Integer, String, Float, Enum, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import TimestampMixin
from app.db.session import Base
import enum

class PlatformEnum(enum.Enum):
    IMDB = "IMDB"

movie_actor = Table(
    "movie_actor",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("actor_id", Integer, ForeignKey("actors.id", ondelete="CASCADE"), primary_key=True),
)

class Movie(Base, TimestampMixin):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    rating = Column(Float)
    year = Column(Integer)
    duration_minutes = Column(Integer)
    metascore = Column(Integer)
    detail_url = Column(String, nullable=False)
    external_id = Column(String, nullable=False, unique=True)
    platform = Column(Enum(PlatformEnum), nullable=False)

    actors = relationship("Actor", secondary=movie_actor, backref="movies")

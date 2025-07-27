from sqlalchemy import Column, Integer, String
from app.db.base_class import TimestampMixin
from app.db.session import Base

class Actor(Base, TimestampMixin):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

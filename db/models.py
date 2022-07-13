from sqlalchemy import Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base

from bot.init_bot import engine

Base = declarative_base()


class Cities(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False, unique=True)
    link = Column(String(300), nullable=False)
    population = Column(Integer, nullable=False)


Base.metadata.create_all(engine)

import datetime
from sqlalchemy import Integer, DateTime, Boolean
from sqlalchemy.sql.schema import Column
from database import Base


class Brew(Base):
    __tablename__ = 'brews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    startOrStop = Column(Boolean, nullable=False, default=True)

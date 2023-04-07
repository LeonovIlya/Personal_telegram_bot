import datetime as DT

from sqlalchemy import create_engine, Column, Integer,\
    Boolean, String, DateTime
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker

import config


engine = create_engine(
    f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}:{config.DB_PORT}"
    f"/{config.DB_NAME}")

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class Reminder(Base):
    __tablename__ = 'reminder_db'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    text = Column(String)
    entry_time = Column(DateTime, default=DT.datetime.now)
    reminder_time = Column(DateTime, default=DT.datetime.now)
    done = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)

from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy.ext.automap import automap_base

POSTGRES_URI="postgresql+psycopg2://datahub_postgres:Password123!@postgressqlfordatahub.postgres.database.azure.com/master_data_supermarker_app?sslmode=require"

engine = create_engine(POSTGRES_URI, echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()


# Database Dependency
def get_postgres_db():
    Base = declarative_base()
    db = Session()
    try:
        yield db
    finally:
        db.close()

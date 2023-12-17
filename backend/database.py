from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# https://fastapi.tiangolo.com/tutorial/sql-databases/

# For persistent storage, a persistent volume is used
SQLALCHEMY_DATABASE_URL = "sqlite:///./weather_data.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///data/weather_data.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
SQLALCHEMY_DATBASE_URL = "sqlite:///./todos.db"

# Create a sql alchemy engine
engine = create_engine(SQLALCHEMY_DATBASE_URL)

# Create an instance of session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# initialize a base that will control db
Base = declarative_base()


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
SQLALCHEMY_DATBASE_URL = "mysql+pymysql://root:admin@127.0.0.1:3306/todo_app_db"

# Create a sql alchemy engine
engine = create_engine(SQLALCHEMY_DATBASE_URL)

# Create an instance of session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# initialize a base that will control db
Base = declarative_base()


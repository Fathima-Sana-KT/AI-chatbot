from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

# PostgreSQL Setup
DATABASE_URL = "postgresql://user:password@localhost/ktudb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
mongo_db = client["ktudata"]


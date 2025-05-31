from sqlmodel import create_engine, Session
import os
import pandas as pd
from db.models import SQLModel


# Database setup
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///db/{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    """Create a new SQLModel session."""
    yield Session(engine)
    
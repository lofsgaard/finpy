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

def import_data():
    column_map = {
        "Dato": "dato",
        "Inn på konto": "inn",
        "Ut fra konto": "ut",
        "Til konto": "tilkonto",
        "Til kontonummer": "tilkonto_nr",
        "Fra konto": "frakonto",
        "Fra kontonummer": "frakonto_nr",
        "Type": "type",
        "Tekst": "tekst",
        "KID": "kid",
        "Hovedkategori": "hovedkategori",
        "Underkategori": "underkategori"
    }
    
    files = os.listdir("db/data")
    for file in files:
        if file.endswith(".csv"):
            print(f"Importing data from {file}")
            df = pd.read_csv(os.path.join("db/data", file), sep=";", encoding="utf-8", decimal=",")
            df = df.rename(columns=column_map)
            pd.to_numeric(df["kid"], errors="coerce")
            df['dato'] = pd.to_datetime(df['dato']).dt.date
            df = df.astype({
                "inn": "float64",
                "ut": "float64",
                })
            sqlite_connection = engine.connect()
            df.to_sql("transactions", sqlite_connection, if_exists="append", index=False)
            sqlite_connection.close()
# FinPy

FinPy is a FastAPI-based application for importing, storing, and serving bank transaction data from CSV files. It uses SQLModel for ORM/database access and pandas for data import and transformation.

## Features

- Imports transaction data from CSV files in the `db/data/` directory.
- Maps and cleans up CSV columns to match the `Transactions` database model.
- Stores transactions in a SQLite database (`db/database.db`).
- Provides a REST API endpoint to fetch all transactions.

## Project Structure

```
main.py                # FastAPI app entry point
db/
  db.py                # Database setup, import logic, session management
  models.py            # SQLModel data models
  data/                # Place your CSV files here
README.md              # This file
```

## How It Works

1. **Data Import:**

   - Place your CSV files (with columns like "Dato", "Inn på konto", etc.) in `db/data/`.
   - When you run the app, it reads these files, remaps columns, converts data types, and imports them into the SQLite database.

2. **Database:**

   - The database schema is defined in `db/models.py` using SQLModel.
   - The database file is located at `db/database.db`.

3. **API:**
   - The FastAPI app exposes a `/transactions` endpoint that returns all transactions as JSON.

## Setup & Usage

1. **Install dependencies:**

   ```zsh
   uv pip install -r uv.lock
   ```

2. **Run the application to create database and import:**

   ```zsh
   uv run main.py
   ```

   This will:

   - Create the database and tables (if not present)
   - Import data from CSV files in `db/data/`

3. **Start the API server:**

   ```zsh
   uv run fastapi dev

   ```

   The API will be available at [http://127.0.0.1:8000/transactions](http://127.0.0.1:8000/transactions).

## Customization

- To add more CSV files, simply place them in `db/data/` and rerun the import.
- Adjust the column mapping in `db/db.py` if your CSV format changes.

## Requirements

- Python 3.13+
- FastAPI
- SQLModel
- pandas
- [uv](https://github.com/astral-sh/uv)

## License

MIT License

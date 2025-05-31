# FinPy

FinPy is a FastAPI-based application for importing, storing, updating, and serving bank transaction data from CSV files. It uses SQLModel for ORM/database access and pandas for data import and transformation.

## Features

- Imports transaction data from CSV files in the `db/data/` directory or via the `/transactions` upload endpoint.
- Maps and cleans up CSV columns to match the `Transactions` database model.
- Stores transactions in a SQLite database (`db/database.db`).
- Provides a REST API endpoint to fetch all transactions or a single transaction by ID.
- Supports updating transaction categories (hovedkategori/underkategori) via dedicated endpoints.
- Allows deleting transactions by ID.

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

   - Upload a CSV file via the `/transactions` POST endpoint to import transactions. The app reads the uploaded file, remaps columns, converts data types, and imports them into the SQLite database.

2. **Database:**

   - The database schema is defined in `db/models.py` using SQLModel.
   - The database file is located at `db/database.db`.

3. **API:**
   - `GET /transactions` — Returns all transactions as JSON.
   - `GET /transactions/{transaction_id}` — Returns a single transaction by ID.
   - `POST /transactions` — Upload a CSV file to import transactions.
   - `POST /transactions/hoved/{transaction_id}` — Update the hovedkategori (main category) of a transaction.
   - `POST /transactions/under/{transaction_id}` — Update the underkategori (subcategory) of a transaction.
   - `DELETE /transactions/{transaction_id}` — Delete a transaction by ID.

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

3. **Start the API server:**

   ```zsh
   uv run fastapi dev
   ```

   The API will be available at [http://127.0.0.1:8000/transactions](http://127.0.0.1:8000/transactions).

## Customization

- Adjust the column mapping in `db/db.py` if your CSV format changes.

## Requirements

- Python 3.13+
- FastAPI
- SQLModel
- pandas
- [uv](https://github.com/astral-sh/uv)

## License

MIT License

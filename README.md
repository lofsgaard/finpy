# FinPy

FinPy is a FastAPI-based application for importing, storing, updating, and serving bank transaction data from CSV files. It uses SQLModel for ORM/database access and pandas for data import and transformation.

## Features

- Import transaction data via the `/transactions` upload endpoint (CSV file upload).
- Maps and cleans up CSV columns to match the `Transactions` database model.
- Stores transactions in a SQLite database.
- Provides REST API endpoints to fetch all transactions or a single transaction by ID.
- Supports updating transaction categories (hovedkategori/underkategori) via dedicated endpoints.
- Allows deleting transactions by ID.

## Project Structure

```
app/
  api/
    main.py                # API router entry point
    routes/
      transactions.py      # All transaction-related endpoints
  db/
    db.py                  # Database setup, session management, import logic
    models.py              # SQLModel data models
  core/
    config.py              # App configuration (if present)
README.md                  # This file
```

### Example: API Router Setup

```python
# filepath: /Users/andreas/Code/finpy/app/api/main.py
from fastapi import APIRouter
from app.api.routes import transactions

api_router = APIRouter()
api_router.include_router(transactions.router)
```

## How It Works

1. **Data Import:**

   - Upload a CSV file via the `/transactions` POST endpoint to import transactions. The app reads the uploaded file, remaps columns, converts data types, and imports them into the SQLite database.

2. **Database:**

   - The database schema is defined in `app/db/models.py` using SQLModel.

3. **API Endpoints:**
   - `GET /transactions` — Returns all transactions as JSON.
   - `GET /transactions/{transaction_id}` — Returns a single transaction by ID.
   - `POST /transactions` — Upload a CSV file to import transactions.
   - `POST /transactions/hoved/{transaction_id}` — Update the hovedkategori (main category) of a transaction.
   - `POST /transactions/under/{transaction_id}` — Update the underkategori (subcategory) of a transaction.
   - `DELETE /transactions/{transaction_id}` — Delete a transaction by ID.

## Setup & Usage

1. **Install dependencies:**

   ```zsh
   uv sync
   ```

2. **Run the application to create database and import:**

   ```zsh
   uv run app/main.py
   ```

   This will:

   - Create the database and tables (if not present)

3. **Start the API server:**

   ```zsh
   uv run fastapi dev
   ```

   The API docs will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Requirements

- Python 3.13+
- FastAPI
- SQLModel
- pandas
- uvicorn
- uv (for dependency management)
- psycopg

## License

MIT License

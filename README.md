# FinPy

FinPy is a modern financial transaction management system built with FastAPI, SQLModel, and Streamlit. It allows you to import, store, update, and analyze bank transaction data from CSV files, and provides both a REST API and a Streamlit dashboard for data exploration.

## Features

- Import transaction data via a `/transactions` upload endpoint (CSV file upload)
- Store transactions in a PostgreSQL or SQLite database using SQLModel
- REST API endpoints to fetch all transactions, fetch by year, fetch by ID, update categories, and delete
- Streamlit dashboard for interactive data analysis and visualization
- Customizable column mapping and category management

## Project Structure

```
app/
  api/
    main.py                # API router entry point
    routes/
      transactions.py      # All transaction-related endpoints
  core/
    config.py              # App configuration
    db/
      db.py                # Database setup, session management, import logic
      models.py            # SQLModel data models
frontend/
  main.py                  # Streamlit dashboard
README.md                  # This file
alembic/                   # Database migrations
pyproject.toml             # Project dependencies and settings
uv.lock                    # uv dependency lock file
```

## How It Works

### Data Import

- Upload a CSV file via the `/transactions` POST endpoint to import transactions. The app reads the uploaded file, remaps columns, converts data types, and imports them into the database.

### Database

- The database schema is defined in `app/core/db/models.py` using SQLModel.
- Database migrations are managed with Alembic (`alembic/`).

### API Endpoints

- `GET /transactions` — Returns all transactions as JSON
- `GET /transactions/{transaction_id}` — Returns a single transaction by ID
- `GET /transactions/year/{year}` — Returns all transactions for a given year
- `POST /transactions` — Upload a CSV file to import transactions
- `PUT /transactions/hovedkategori/{transaction_id}` — Update the hovedkategori (main category) of a transaction
- `PUT /transactions/underkategori/{transaction_id}` — Update the underkategori (subcategory) of a transaction
- `DELETE /transactions/{transaction_id}` — Delete a transaction by ID

### Streamlit Dashboard

- The dashboard in `frontend/main.py` lets you search, filter, and summarize transactions by year, store, and category.
- Summaries and totals are shown for selected stores and categories.

## Setup & Usage

1. **Install dependencies:**

   ```sh
   uv sync
   ```

2. **Run database migrations (if using PostgreSQL):**

   ```sh
   alembic upgrade head
   ```

3. **Run the FastAPI application:**

   ```sh
   uvicorn app.main:app --reload
   ```

   The API docs will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

4. **Run the Streamlit dashboard:**
   ```sh
   streamlit run frontend/main.py
   ```

## Requirements

- Python 3.13+
- FastAPI
- SQLModel
- pandas
- uvicorn
- uv (for dependency management)
- psycopg (for PostgreSQL)
- streamlit

## License

MIT License

from fastapi import FastAPI

from app.core.db.db import create_db_and_tables
from app.api.main import api_router
from app.core.config import settings

app = FastAPI()

app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    create_db_and_tables()

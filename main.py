from fastapi import FastAPI, Depends
from db.db import create_db_and_tables, import_data, get_session
from db.models import Transactions
from sqlmodel import Session, select

app = FastAPI()

@app.get("/transactions")
async def get_transactions(session: Session = Depends(get_session)) -> list[Transactions]:
    with session:
        result = session.exec(select(Transactions)).all()
        return result

if __name__ == "__main__":
    create_db_and_tables()
    import_data()

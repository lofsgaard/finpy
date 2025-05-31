from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from db.db import create_db_and_tables, get_session, engine
from db.models import Transactions, TransactionUpdateHoved, TransactionUpdateUnder
from sqlmodel import Session, select
import pandas as pd
import io
from collections import OrderedDict


app = FastAPI()

@app.get("/transactions", response_model=list[Transactions])
async def get_transactions(session: Session = Depends(get_session)):
    with session:
        result = session.exec(select(Transactions)).all()
        ordered = [
            OrderedDict([
                ("id", t.id),
                ("dato", t.dato),
                ("inn", t.inn),
                ("ut", t.ut),
                ("tilkonto", t.tilkonto),
                ("tilkonto_nr", t.tilkonto_nr),
                ("frakonto", t.frakonto),
                ("frakonto_nr", t.frakonto_nr),
                ("type", t.type),
                ("tekst", t.tekst),
                ("kid", t.kid),
                ("hovedkategori", t.hovedkategori),
                ("underkategori", t.underkategori),
            ]) for t in result
        ]
        return ordered
    
@app.get("/transactions/{transaction_id}", response_model=Transactions)
async def get_transaction(transaction_id: int, session: Session = Depends(get_session)):
    with session:
        transaction = session.get(Transactions, transaction_id)
        if transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction
    

@app.post("/transactions/hoved/{transaction_id}")
async def update_transaction(transaction_id: int, transaction: TransactionUpdateHoved, session: Session = Depends(get_session)):
    with session:
        existing_transaction = session.get(Transactions, transaction_id)
        if existing_transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        for key, value in transaction.model_dump(exclude_unset=True).items():
            setattr(existing_transaction, key, value)
        
        session.add(existing_transaction)
        session.commit()
        session.refresh(existing_transaction)
        return session.get(Transactions, transaction_id)
    
@app.post("/transactions/under/{transaction_id}")
async def update_transaction(transaction_id: int, transaction: TransactionUpdateUnder, session: Session = Depends(get_session)):
    with session:
        existing_transaction = session.get(Transactions, transaction_id)
        if existing_transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        for key, value in transaction.model_dump(exclude_unset=True).items():
            setattr(existing_transaction, key, value)
        
        session.add(existing_transaction)
        session.commit()
        session.refresh(existing_transaction)
        return session.get(Transactions, transaction_id)
    
@app.delete("/transactions/{transaction_id}")
async def delete_transaction(transaction_id: int, session: Session = Depends(get_session)):
    with session:
        transaction = session.get(Transactions, transaction_id)
        if transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        session.delete(transaction)
        session.commit()
        return {"message": "Transaction deleted successfully"}
    
@app.post("/transactions")
async def upload_transactions(file: UploadFile = File(...)):
    if file.content_type == "text/csv":
        try:
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
            contents = await file.read()
            df = pd.read_csv(io.StringIO(contents.decode("utf-8")), sep=";", decimal=",", encoding="utf-8")
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
            return {"message": "Transactions uploaded successfully"}
        except Exception as e:
            return {"error": f"An error occurred while processing the file: {str(e)}"}
    else:
        return {"error": "File must be a CSV file."}


if __name__ == "__main__":
    create_db_and_tables()

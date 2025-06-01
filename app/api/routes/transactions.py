from app.core.db.db import  get_session, engine
from app.core.db.models import Transactions
from sqlmodel import Session, select, cast, String
from fastapi import Depends, UploadFile, File, HTTPException, APIRouter, HTTPException
import pandas as pd
import io
from app.models import TransactionsReturnModel, TransactionUpdateHovedReturnModel, TransactionUpdateUnderReturnModel

router = APIRouter(prefix="/transactions", tags=["transcations"])


@router.get("/", response_model=list[TransactionsReturnModel])
async def get_transactions(session: Session = Depends(get_session)):
    with session:
        result = session.exec(select(Transactions)).all()
        if not result:
            raise HTTPException(status_code=404, detail="No data found")
        return result
    
@router.get("/{transaction_id}", response_model=TransactionsReturnModel)
async def get_transaction(transaction_id: int, session: Session = Depends(get_session)):
    with session:
        transaction = session.get(Transactions, transaction_id)
        if transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction


@router.get("/year/{year}", response_model=list[TransactionsReturnModel])
async def get_transactions_by_date(year: str, session: Session = Depends(get_session)):
    with session:
        try:
            stmt = select(Transactions).where(cast(Transactions.dato, String).like(f"{year}-%"))
            result = session.exec(stmt).all()
            if not result:
                raise HTTPException(status_code=404, detail="No transactions found for this date")
            return result
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")


@router.put("/hovedkategori/{transaction_id}", response_model = TransactionsReturnModel)
async def update_transaction(transaction_id: int, hovedkategori: TransactionUpdateHovedReturnModel, session: Session = Depends(get_session)):
    with session:
        transaction = session.get(Transactions, transaction_id)
        if transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        transaction.hovedkategori = hovedkategori.hovedkategori
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return session.get(Transactions, transaction_id)
    
@router.put("/underkategori/{transaction_id}", response_model = TransactionsReturnModel)
async def update_transaction(transaction_id: int, underkategori: TransactionUpdateUnderReturnModel, session: Session = Depends(get_session)):
    with session:
        transaction = session.get(Transactions, transaction_id)
        if transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        transaction.underkategori = underkategori.hovedkategori
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return session.get(Transactions, transaction_id)
    
@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: int, session: Session = Depends(get_session)):
    with session:
        transaction = session.get(Transactions, transaction_id)
        if transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        session.delete(transaction)
        session.commit()
        return {"message": "Transaction deleted successfully"}
    
@router.post("/")
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
            df['dato'] = pd.to_datetime(df['dato']).dt.date
            sqlite_connection = engine.connect()
            df.to_sql("transactions", sqlite_connection, if_exists="append", index=False)
            sqlite_connection.close()
            return {"message": "Transactions uploaded successfully"}
        except Exception as e:
            return {"error": f"An error occurred while processing the file"}
    else:
        return {"error": "File must be a CSV file."}
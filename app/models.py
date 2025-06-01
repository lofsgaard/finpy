from sqlmodel import SQLModel
from datetime import date


class TransactionsReturnModel(SQLModel):
    id: int 
    dato: date
    inn: float | None  
    ut: float | None
    tilkonto: str | None 
    tilkonto_nr: int | None 
    frakonto: str | None 
    frakonto_nr: int | None 
    type: str 
    tekst: str | None 
    kid: str | None 
    hovedkategori: str | None 
    underkategori: str | None 

class TransactionUpdateHovedReturnModel(SQLModel):
    hovedkategori: str

class TransactionUpdateUnderReturnModel(SQLModel):
    underkategori: str
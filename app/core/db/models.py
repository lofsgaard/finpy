from sqlmodel import Field, SQLModel
from datetime import date

class Transactions(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    dato: date
    inn: float | None = None
    ut: float | None = None
    tilkonto: str | None = None
    tilkonto_nr: int | None = None
    frakonto: str | None = None
    frakonto_nr: int | None = None
    type: str
    tekst: str | None = None
    kid: str | None = None
    hovedkategori: str | None = None
    underkategori: str | None = None


class TransactionUpdateHoved(SQLModel):
    hovedkategori: str | None = None

class TransactionUpdateUnder(SQLModel):
    underkategori: str | None = None
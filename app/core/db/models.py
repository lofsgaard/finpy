from sqlmodel import Field, SQLModel, Column
from sqlalchemy import BigInteger
from datetime import date
from decimal import Decimal

class Transactions(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    dato: date
    inn: Decimal | None  = Field(default=None, max_digits=10, decimal_places=2)
    ut: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    tilkonto: str | None = Field(default=None, max_length=255)
    tilkonto_nr: int | None = Field(default=None, max_length=255, sa_column=Column(BigInteger()))
    frakonto: str | None = Field(default=None, max_length=255)
    frakonto_nr: int | None = Field(default=None, max_length=255, sa_column=Column(BigInteger()))
    type: str = Field(max_length=255)
    tekst: str | None = Field(default=None, max_length=255)
    kid: str | None = Field(default=None, max_length=255)
    hovedkategori: str | None = Field(default=None, max_length=255)
    underkategori: str | None = Field(default=None, max_length=255)


class TransactionUpdateHoved(SQLModel):
    hovedkategori: str

class TransactionUpdateUnder(SQLModel):
    underkategori: str
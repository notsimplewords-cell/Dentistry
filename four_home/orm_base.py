from sqlmodel import SQLModel, Field, Session, select, func
from datetime import date 
from typing import Optional

class patients(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str
    email: str = Field(index=True, unique=True)
    birth_date: Optional[date] = None
    hashed_password: str

class doctor(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str
    email: str = Field(index=True, unique=True)
    birth_date: Optional[date] = None
    specialization: str
    experience: int
    hashed_password: str
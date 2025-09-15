from sqlmodel import SQLModel, Field, Session, select, func
from datetime import date 
from typing import Optional

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str
    email: str = Field(index=True, unique=True)
    birth_date: Optional[date] = None # заменяем age на дату рождения
    hashed_password: str # поле для хэша пароля
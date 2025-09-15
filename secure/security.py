from sqlmodel import SQLModel, Field, create_engine
from typing import Optional


class User(SQLModel, table=True):
    __tablename__ = "user"
    
    id: int = Field(primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    age: Optional[int] = None


class Product(SQLModel, table=True):
    __tablename__ = "product"
    
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    description: Optional[str] = None
    price: float


# Database configuration
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables
SQLModel.metadata.create_all(engine)




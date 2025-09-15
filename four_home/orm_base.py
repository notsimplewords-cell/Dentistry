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

class doctor(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str
    email: str = Field(index=True, unique=True)
    birth_date: Optional[date] = None
    specialization: str
    experience: int
    hashed_password: str

class visit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    doctor_id: int = Field(foreign_key="doctor.id")
    visit_date: date
    complaints: Optional[str] = None
    diagnosis: Optional[str] = None

class prescription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    visit_id: int = Field(foreign_key="visit.id")
    medicine: str
    dose: str
    instructions: Optional[str] = None

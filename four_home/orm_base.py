from sqlmodel import SQLModel, Field, Session, create_engine, Relationship
from datetime import date
from typing import Optional, List

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str = Field(index=True, unique=True)
    birth_date: Optional[date] = None
    hashed_password: str

class Doctor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str = Field(index=True, unique=True)
    birth_date: Optional[date] = None
    specialization: str
    experience: int
    hashed_password: str

class Visit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    doctor_id: int = Field(foreign_key="doctor.id")
    visit_date: date
    complaints: Optional[str] = None
    diagnosis: Optional[str] = None

class Prescription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    visit_id: int = Field(foreign_key="visit.id")
    medicine: str
    dose: str
    instructions: Optional[str] = None



sqlite_file_name = "four_home/dentistry.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)

from sqlmodel import select

with Session(engine) as session:
    # -------------------- Добавление данных --------------------
    patient = Patient(
        username="Pavel",
        email="pavel@example.com",
        birth_date=date(2000, 1, 1),
        hashed_password="123456"
    )
    session.add(patient)

    doctor = Doctor(
        username="Dr.Smith",
        email="smith@example.com",
        birth_date=date(1980, 5, 20),
        specialization="Стоматолог",
        experience=10,
        hashed_password="abcdef"
    )
    session.add(doctor)
    session.commit()

    visit = Visit(
        patient_id=patient.id,
        doctor_id=doctor.id,
        visit_date=date.today(),
        complaints="Болит зуб",
        diagnosis="Кариес"
    )
    session.add(visit)
    session.commit()

    prescription = Prescription(
        visit_id=visit.id,
        medicine="Антибиотик",
        dose="2 раза в день",
        instructions="После еды"
    )
    session.add(prescription)
    session.commit()

    # -------------------- Примеры запросов --------------------

    # 1️⃣ Все пациенты
    patients = session.exec(select(Patient)).all()
    print("Все пациенты:")
    for p in patients:
        print(p)

    # 2️⃣ Пациенты с конкретным email
    pavel = session.exec(select(Patient).where(Patient.email == "pavel@example.com")).first()
    print("\nПациент с email pavel@example.com:", pavel)

    # 3️⃣ Все визиты конкретного пациента
    visits_of_pavel = session.exec(select(Visit).where(Visit.patient_id == patient.id)).all()
    print("\nВизиты Павла:")
    for v in visits_of_pavel:
        print(v)

    # 4️⃣ Все назначения для визита
    prescriptions_for_visit = session.exec(select(Prescription).where(Prescription.visit_id == visit.id)).all()
    print("\nНазначения для визита:")
    for pr in prescriptions_for_visit:
        print(pr)

    # 5️⃣ Соединение: доктор и его визиты
    doctor_visits = session.exec(
        select(Visit, Doctor).where(Visit.doctor_id == Doctor.id)
    ).all()
    print("\nВизиты докторов:")
    for v, d in doctor_visits:
        print(f"Доктор: {d.username}, Визит ID: {v.id}, Диагноз: {v.diagnosis}")
    

    start_date = date(2025, 1, 1)
    end_date = date(2025, 12, 31)
    stmt = select(Visit).where(Visit.visit_date.between(start_date, end_date))
    visits_in_year = session.exec(stmt).all()
    print(f"\nВизиты в 2025 году ({len(visits_in_year)} шт.):")
    for v in visits_in_year:
        print(v)

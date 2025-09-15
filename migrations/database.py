import psycopg2
from argon2 import PasswordHasher
# Инициализация хэшера Argon2
ph = PasswordHasher()
# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
dbname='med.sql',
user='postgres',
password='mavuika',
host='localhost',
port=5432
)
cursor = conn.cursor()
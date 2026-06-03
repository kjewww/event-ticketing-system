from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

try:
    conn = engine.connect()
    print("Connected to PostgreSQL!")
    conn.close()

except Exception as e:
    print("Connection failed!")
    print(e)
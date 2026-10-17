import getpass
import psycopg
from pathlib import Path
from dotenv import load_dotenv
import os


env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# print(env_path)

def connect_database():
    password = getpass.getpass("PostgreSQL password: ")

    return psycopg.connect(
        host=os.getenv("db_host"),
        port=os.getenv("db_port"),
        dbname=os.getenv("db_name"),
        user=os.getenv("db_user"),
        password=password,
    )
    
    
    
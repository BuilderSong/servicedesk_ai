import getpass

import psycopg


def connect_database():
    password = getpass.getpass("PostgreSQL password: ")

    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="warranty_db",
        user="postgres",
        password=password,
    )
    
    
    
    
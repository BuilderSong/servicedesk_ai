from fastapi import FastAPI
from lesson4_sql_select_and_where.open_requests_postgresql import get_open_requests
from lesson4_sql_select_and_where.postgresql import connect_database

app = FastAPI()

@app.get("/")
def home():
    return {"message":"Warranty API is running"}

@app.get("/health")
def health():
    return {"status":"ok", "mode":"synthetic"}

@app.get("/properties/{property_id}/requests")
def get_requests(property_id):
    try:
        with connect_database() as conn:
         return get_open_requests(conn, property_id)
    except Exception as e:
        print(e)
            
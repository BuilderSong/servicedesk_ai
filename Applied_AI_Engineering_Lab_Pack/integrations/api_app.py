"""Local teaching service: synthetic reads only, no authentication."""
from fastapi import FastAPI
from solutions.core import database, open_requests
app = FastAPI(title="ServiceDesk Course - local synthetic demo")

@app.get("/health")
def health():
    return {"status":"ok", "mode":"synthetic"}

@app.get("/properties/{property_id}/requests")
def requests(property_id: int):
    conn=database()
    try:
        return {"items":[{"id":i,"text":t} for i,t in open_requests(conn,property_id)]}
    finally:
        conn.close()

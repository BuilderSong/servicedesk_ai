# Connect the ServiceDesk frontend to FastAPI

Download index.html from the dashboard footer and place it in a frontend folder beside your FastAPI module.

Add these imports and route to your existing module (keep both existing API routes):

```python
from pathlib import Path
from fastapi.responses import FileResponse

FRONTEND = Path(__file__).resolve().parent / "frontend"

@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(FRONTEND / "index.html")
```

Run your existing Uvicorn command, then open http://127.0.0.1:8000/.
In Connection settings, choose FastAPI and leave API base URL blank.
This serves frontend and API from the same origin without CORS changes.

Optional: place this guide in the frontend folder and add a GET /integration.md
FileResponse route if you want its footer link to work locally too.

The dashboard calls GET /health and GET /properties/{property_id}/requests.
It expects {"items": [{"id": 1, "text": "Description"}]}.
Status is displayed as Open because this endpoint returns open requests.
Demo records are illustrative and are not inferred from your database.
No request creation, editing, authentication, or persistent database changes are implemented.

A deployed HTTPS preview may not be able to call a local HTTP API due to browser
local network or mixed-content restrictions. Serving from FastAPI is the recommended
local setup. A separate frontend origin requires a specifically allowed CORS origin.
Do not expose this unauthenticated teaching API as a production service.

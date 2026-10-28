"""Run from the project root: python -m uvicorn lesson6_authentication.api_app:app --reload"""

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Response

from lesson6_authentication.demo_store import (
    WarrantyRequest,
    close_request,
    find_request,
    get_open_requests,
)
from lesson6_authentication.security import (
    LoginInput,
    TokenResponse,
    User,
    authenticate_user,
    check_property_access,
    create_access_token,
    get_current_user,
    require_technician,
)


app = FastAPI(title="Warranty Authentication Lesson")


@app.get("/health")
def health():
    return {"status": "ok", "mode": "synthetic"}


@app.post("/login", response_model=TokenResponse)
def login(data: LoginInput, response: Response):
    user = authenticate_user(data.username, data.password.get_secret_value())
    response.headers["Cache-Control"] = "no-store"
    return TokenResponse(access_token=create_access_token(user.username))


@app.get("/me", response_model=User)
def me(user: Annotated[User, Depends(get_current_user)]):
    return user


@app.get("/properties/{property_id}/requests")
def requests(
    property_id: int,
    user: Annotated[User, Depends(get_current_user)],
):
    check_property_access(user, property_id)
    return {"items": get_open_requests(property_id)}


@app.patch("/requests/{request_id}/close", response_model=WarrantyRequest)
def close(
    request_id: int,
    user: Annotated[User, Depends(require_technician)],
):
    item = find_request(request_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Warranty request not found")

    # A technician must ALSO have permission for this particular property.
    check_property_access(user, item.property_id)
    return close_request(item)

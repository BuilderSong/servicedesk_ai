  # routes, strict schema, identity dependency
  
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr

from lesson6_api_architecture import service
from lesson6_api_architecture.domain import (
    DomainValidationError, Identity, PropertyNotFound, RequestNotFound,
)
from lesson6_api_architecture.repository import PostgresRequestRepository, RequestRepository
from lesson4_sql_select_and_where.postgresql import connect_database

app = FastAPI()


# ---- schemas (shape only) ----
class RequestCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")  # organization_id in the body -> 422

    property_id: StrictInt = Field(gt=0, examples=[101])
    description: StrictStr = Field(examples=["Leaking basement window"])


class RequestOut(BaseModel):
    id: int
    property_id: int
    description: str
    status: str


class ErrorResponse(BaseModel):
    detail: str


# ---- test identities: each belongs to exactly one organization ----
TEST_IDENTITIES = {
    "alice": Identity(user_id="alice", organization_id=1),
    "bob": Identity(user_id="bob", organization_id=2),
}


def get_identity(x_test_user: Annotated[str | None, Header()] = None) -> Identity:
    identity = TEST_IDENTITIES.get(x_test_user or "")
    if identity is None:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    return identity


def get_repository() -> RequestRepository:
    return PostgresRequestRepository(connect_database)


Repo = Annotated[RequestRepository, Depends(get_repository)]
Caller = Annotated[Identity, Depends(get_identity)]


# ---- domain errors -> HTTP ----
@app.exception_handler(DomainValidationError)
def _domain_validation(_, exc: DomainValidationError):
    return JSONResponse(status_code=422, content={"detail": str(exc)})


@app.exception_handler(PropertyNotFound)
def _property_not_found(_, exc):
    return JSONResponse(status_code=404, content={"detail": "Property not found"})


@app.exception_handler(RequestNotFound)
def _request_not_found(_, exc):
    return JSONResponse(status_code=404, content={"detail": "Request not found"})


# ---- routes ----
@app.get("/")
def home():
    return {"message": "Warranty API is running"}


@app.get("/health")
def health():
    return {"status": "ok", "mode": "synthetic"}


@app.post(
    "/requests",
    status_code=201,
    response_model=RequestOut,
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse, "description": "Unknown property, or one in another organization."},
        422: {"description": "Bad shape (Pydantic) or bad business value (domain)."},
    },
)
def create_request(payload: RequestCreate, repo: Repo, identity: Caller):
    return service.create_request(repo, identity, payload.property_id, payload.description)


@app.get(
    "/requests/{request_id}",
    response_model=RequestOut,
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def get_request(request_id: int, repo: Repo, identity: Caller):
    return service.get_request(repo, identity, request_id)


@app.get(
    "/properties/{property_id}/requests",
    response_model=list[RequestOut],
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def list_open_requests(property_id: int, repo: Repo, identity: Caller):
    found = repo.list_open(
        organization_id=identity.organization_id, property_id=property_id
    )
    if found is None:
        raise PropertyNotFound()
    return found
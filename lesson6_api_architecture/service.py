  # business rules (application logic)
  
from lesson6_api_architecture.domain import (
    DomainValidationError, Identity, RequestNotFound, WarrantyRequest,
)
from lesson6_api_architecture.repository import RequestRepository

MAX_DESCRIPTION = 1000


def create_request(
    repo: RequestRepository, identity: Identity, property_id: int, description: str
) -> WarrantyRequest:
    cleaned = description.strip()
    if not cleaned:
        raise DomainValidationError("description must not be blank")
    if len(cleaned) > MAX_DESCRIPTION:
        raise DomainValidationError(
            f"description must be at most {MAX_DESCRIPTION} characters"
        )
    # Org comes from the identity. The caller never supplies it.
    return repo.create_request(
        organization_id=identity.organization_id,
        property_id=property_id,
        description=cleaned,
        created_by=identity.user_id,
    )


def get_request(
    repo: RequestRepository, identity: Identity, request_id: int
) -> WarrantyRequest:
    found = repo.get_request(
        organization_id=identity.organization_id, request_id=request_id
    )
    if found is None:
        raise RequestNotFound()
    return found
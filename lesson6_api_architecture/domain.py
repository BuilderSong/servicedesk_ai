# Identity, WarrantyRequest, errors

from dataclasses import dataclass


class DomainValidationError(Exception):
    pass


class PropertyNotFound(Exception):
    pass


class RequestNotFound(Exception):
    pass


@dataclass(frozen=True)
class Identity:
    user_id: str
    organization_id: int


@dataclass(frozen=True)
class WarrantyRequest:
    id: int
    property_id: int
    description: str
    status: str
    created_by: str
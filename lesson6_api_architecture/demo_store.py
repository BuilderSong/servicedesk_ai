"""Synthetic practice records. Reloading the server resets these records."""

from typing import Literal

from pydantic import BaseModel


class WarrantyRequest(BaseModel):
    id: int
    property_id: int
    description: str
    status: Literal["open", "closed"]
    version: int = 1


REQUESTS = {
    105: WarrantyRequest(id=105, property_id=3, description="Window handle is loose", status="open"),
    106: WarrantyRequest(id=106, property_id=3, description="Drywall crack", status="closed", version=2),
    201: WarrantyRequest(id=201, property_id=4, description="Front door does not latch", status="open"),
}


def get_open_requests(property_id: int) -> list[WarrantyRequest]:
    return [
        item for item in REQUESTS.values()
        if item.property_id == property_id and item.status == "open"
    ]


def find_request(request_id: int) -> WarrantyRequest | None:
    return REQUESTS.get(request_id)


def close_request(item: WarrantyRequest) -> WarrantyRequest:
    if item.status == "open":
        item.status = "closed"
        item.version += 1
    return item

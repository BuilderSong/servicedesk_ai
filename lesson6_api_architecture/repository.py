# Protocol + Postgres implementation

from typing import Callable, Protocol

from lesson6_api_architecture.domain import PropertyNotFound, WarrantyRequest

_COLS = "r.id, r.property_id, r.description, r.status, r.created_by"


class RequestRepository(Protocol):
    def create_request(
        self, *, organization_id: int, property_id: int,
        description: str, created_by: str,
    ) -> WarrantyRequest: ...

    def get_request(
        self, *, organization_id: int, request_id: int
    ) -> WarrantyRequest | None: ...

    def list_open(
        self, *, organization_id: int, property_id: int
    ) -> list[WarrantyRequest] | None: ...


class PostgresRequestRepository:
    def __init__(self, connect: Callable):
        self._connect = connect  # e.g. your connect_database

    def create_request(self, *, organization_id, property_id, description, created_by):
        # One statement: the insert only happens if the property is in this org.
        sql = """
            INSERT INTO requests (property_id, description, created_by)
            SELECT p.id, %s, %s
            FROM properties p
            WHERE p.id = %s AND p.organization_id = %s
            RETURNING id, property_id, description, status, created_by
        """
        with self._connect() as conn:  # commits on success, rolls back on error
            with conn.cursor() as cur:
                cur.execute(sql, (description, created_by, property_id, organization_id))
                row = cur.fetchone()
        if row is None:
            raise PropertyNotFound()
        return WarrantyRequest(*row)

    def get_request(self, *, organization_id, request_id):
        sql = f"""
            SELECT {_COLS}
            FROM requests r
            JOIN properties p ON p.id = r.property_id
            WHERE r.id = %s AND p.organization_id = %s
        """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (request_id, organization_id))
                row = cur.fetchone()
        return WarrantyRequest(*row) if row else None

    def list_open(self, *, organization_id, property_id):
        visible = "SELECT 1 FROM properties WHERE id = %s AND organization_id = %s"
        sql = f"""
            SELECT {_COLS}
            FROM requests r
            JOIN properties p ON p.id = r.property_id
            WHERE p.id = %s AND p.organization_id = %s AND r.status = 'open'
            ORDER BY r.id
        """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(visible, (property_id, organization_id))
                if cur.fetchone() is None:
                    return None  # unknown OR other org's property
                cur.execute(sql, (property_id, organization_id))
                return [WarrantyRequest(*row) for row in cur.fetchall()]
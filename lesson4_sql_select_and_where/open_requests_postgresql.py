import psycopg
from lesson4_sql_select_and_where.postgresql import connect_database


def get_open_requests(
    conn: psycopg.Connection,
    property_id: int,
) -> list[tuple[int, str]]:
    """Return (request_id, description) pairs for open requests."""
    query = """
        SELECT id, description
        FROM warranty_requests
        WHERE property_id = %s AND status = %s
        ORDER BY id
    """

    with conn.cursor() as cursor:
        cursor.execute(query, (property_id, "open"))
        return cursor.fetchall()


def main() -> None:
    try:
        property_id = int(input("Enter a positive property ID: "))
    except ValueError:
        print("Please enter a valid integer.")
        return

    if property_id <= 0:
        print("Property ID must be greater than zero.")
        return

    with connect_database() as conn:
        requests = get_open_requests(conn, property_id)

    if not requests:
        print("No open requests found.")
        return

    for request_id, description in requests:
        print(f"{request_id}: {description}")


if __name__ == "__main__":
    main()
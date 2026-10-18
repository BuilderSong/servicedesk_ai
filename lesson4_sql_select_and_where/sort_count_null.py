"""Practice nullable columns, counting, and deterministic ordering."""

from datetime import datetime, timezone

from psycopg import Connection

from postgresql import connect_database


def show_results(conn: Connection, title: str, query: str) -> None:
    cursor = conn.execute(query)

    print(f"\n{title}")
    if cursor.description:
        print(" | ".join(column.name for column in cursor.description))

    for row in cursor.fetchall():
        print(" | ".join(
            "NULL" if value is None else str(value)
            for value in row
        ))


def sort_count_null(conn: Connection) -> None:
    # A temporary practice table disappears when this connection closes.
    # WITH NO DATA copies the columns without copying existing requests.
    conn.execute(
        """
        CREATE TEMP TABLE warranty_requests_lab AS
        SELECT *
        FROM warranty_requests
        WITH NO DATA
        """
    )

    # Recreate these columns so the exercise has predictable definitions.
    conn.execute(
        """
        ALTER TABLE warranty_requests_lab
        DROP COLUMN IF EXISTS assigned_to
        """
    )
    conn.execute(
        """
        ALTER TABLE warranty_requests_lab
        ADD COLUMN assigned_to TEXT
        """
    )

    conn.execute(
        """
        ALTER TABLE warranty_requests_lab
        DROP COLUMN IF EXISTS created_at
        """
    )
    conn.execute(
        """
        ALTER TABLE warranty_requests_lab
        ADD COLUMN created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        """
    )

    first_time = datetime(2026, 10, 16, 14, 0, tzinfo=timezone.utc)
    later_time = datetime(2026, 10, 16, 15, 0, tzinfo=timezone.utc)

    requests = [
        (1, 7, "plumbing", "Toilet leaking", "open", None, first_time),
        (2, 7, "electrical", "Outlet not working", "open", "Steven", first_time),
        (3, 7, "painting", "Wall touch-up", "open", "Alex", later_time),
        (4, 7, "plumbing", "Faucet repaired", "closed", "Steven", later_time),
        (5, 7, "doors", "Door sticking", "open", None, later_time),
    ]

    for request in requests:
        conn.execute(
            """
            INSERT INTO warranty_requests_lab (
                id,
                property_id,
                category,
                description,
                status,
                assigned_to,
                created_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            request,
        )

    show_results(
        conn,
        "Unassigned requests",
        """
        SELECT id, description, assigned_to
        FROM warranty_requests_lab
        WHERE assigned_to IS NULL
        ORDER BY id
        """,
    )

    show_results(
        conn,
        "Counts of open requests",
        """
        SELECT
            COUNT(*) AS total_open,
            COUNT(assigned_to) AS assigned_open
        FROM warranty_requests_lab
        WHERE status = 'open'
        """,
    )

    show_results(
        conn,
        "Open requests, oldest first",
        """
        SELECT id, status, assigned_to, created_at
        FROM warranty_requests_lab
        WHERE status = 'open'
        ORDER BY created_at ASC, id ASC
        """,
    )


def main() -> None:
    with connect_database() as conn:
        sort_count_null(conn)


if __name__ == "__main__":
    main()
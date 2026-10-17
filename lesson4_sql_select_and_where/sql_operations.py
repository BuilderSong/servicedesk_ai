from postgresql import connect_database


def main():
    with connect_database() as conn:
        # READ: show open requests.
        rows = conn.execute(
            """
            SELECT id, property_id, description, status
            FROM warranty_requests
            WHERE status = %s
            ORDER BY id;
            """,
            ("open",),
        ).fetchall()

        for row in rows:
            print(row)

        # CREATE: add a request to an existing property.
        property_id = int(input("Existing property ID: "))

        new_request = conn.execute(
            """
            INSERT INTO warranty_requests (
                property_id,
                category,
                description
            )
            VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (
                property_id,
                "plumbing",
                "Practice request: bathroom tap is leaking",
            ),
        ).fetchone()

        request_id = new_request[0] # type: ignore
        print("Created request:", request_id) # type: ignore

        # UPDATE: change the request we just created.
        updated = conn.execute(
            """
            UPDATE warranty_requests
            SET status = %s
            WHERE id = %s
            RETURNING id, status;
            """,
            ("scheduled", request_id), # type: ignore
        ).fetchone()

        print("Updated request:", updated)


if __name__ == "__main__":
    main()
import json
from pathlib import Path
from postgresql import connect_database


DATA_FOLDER = Path(__file__).parent / "documents"


def read_json(filename): # type: ignore
    file_path = DATA_FOLDER / filename # type: ignore
    with file_path.open(encoding="utf-8") as file: # type: ignore
        return json.load(file) # type: ignore


def insert_homeowners(conn, homeowners): # type: ignore
    homeowner_id_map = {}

    for homeowner in homeowners: # type: ignore
        row = conn.execute( # type: ignore
            """
            INSERT INTO homeowners (name, email, phone)
            VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (
                homeowner["name"],
                homeowner["email"],
                homeowner["phone"],
            ),
        ).fetchone()

        homeowner_id_map[homeowner["id"]] = row[0]

    return homeowner_id_map # type: ignore


def insert_properties(conn, properties, homeowner_id_map): # type: ignore
    property_id_map = {}

    for property_record in properties: # type: ignore
        # Translate JSON homeowner IDs into actual database IDs.
        homeowner_ids = [ # type: ignore
            homeowner_id_map[sample_id]
            for sample_id in property_record["homeowner_ids"] # type: ignore
        ]

        row = conn.execute( # type: ignore
            """
            INSERT INTO properties (address, homeowner_ids)
            VALUES (%s, %s)
            RETURNING id;
            """,
            (
                property_record["address"],
                homeowner_ids,
            ),
        ).fetchone()

        property_id_map[property_record["id"]] = row[0]

    return property_id_map # type: ignore


def insert_requests(conn, requests, property_id_map): # type: ignore
    for request in requests: # type: ignore
        # Translate the JSON property ID into its database ID.
        property_id = property_id_map[request["property_id"]] # type: ignore

        conn.execute( # type: ignore
            """
            INSERT INTO warranty_requests (
                property_id,
                category,
                description,
                status
            )
            VALUES (%s, %s, %s, %s);
            """,
            (
                property_id,
                request["category"],
                request["description"],
                request["status"],
            ),
        )


def main():
    homeowners = read_json("homeowners.json")
    properties = read_json("properties.json")
    requests = read_json("warranty_requests.json")
    
    # All inserts belong to one transaction.
    with connect_database() as conn:
        homeowner_id_map = insert_homeowners(conn, homeowners) # type: ignore
        
        property_id_map = insert_properties( # type: ignore
            conn,
            properties,
            homeowner_id_map,
        )

        insert_requests(conn, requests, property_id_map)

    print(
        f"Imported {len(homeowners)} homeowners, "
        f"{len(properties)} properties, "
        f"and {len(requests)} warranty requests."
    )


if __name__ == "__main__":
    main()
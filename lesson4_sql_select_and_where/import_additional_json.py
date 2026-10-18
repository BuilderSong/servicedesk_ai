from postgresql import connect_database
from pathlib import Path
import json

json_files_folder = Path(__file__).resolve().parent/"documents"

def get_additional_data(filename:str):
    with open(json_files_folder/filename, "r", encoding="utf-8") as file:
        return json.load(file)
    
def import_additional_homeowners(conn, homeowners): # type: ignore
    homeowner_id_map = {} # type: ignore
    for homeowner in homeowners: # type: ignore
        row = conn.execute( # type: ignore
            """
            INSERT INTO homeowners (name, email, phone)
            VALUES (%s, %s, %s)
            RETURNING id
            """, (homeowner["name"],homeowner["email"],homeowner["phone"])).fetchone()
        homeowner_id_map[homeowner["id"]] = row[0]
    return homeowner_id_map # type: ignore


def import_additional_properties(conn, properties, homeowner_id_map): # type: ignore
    property_id_map = {}
    for property in properties: # type: ignore
        row = conn.execute( # type: ignore
            """
            INSERT INTO properties (address, homeowner_ids)
            VALUES (%s, %s)
            returning id
            """, (property["address"], [homeowner_id_map[json_id] for json_id in property["homeowner_ids"]])).fetchone()
        property_id_map[property["id"]] = row[0]
    return property_id_map # type: ignore

def import_additional_warranty_requests(conn, warranty_requests, property_id_map):
    for warranty_request in warranty_requests: # type: ignore
        conn.execute( # type: ignore
            """
            INSERT INTO warranty_requests (property_id, category, description, status)
            VALUES (%s, %s, %s, %s)
            """, (property_id_map[warranty_request["property_id"]], warranty_request["category"], warranty_request["description"], warranty_request["status"]))
    return

def main():
    homeowners = get_additional_data("homeowners_additional.json")
    properties = get_additional_data("properties_additional.json")
    warranty_requests = get_additional_data("warranty_requests_additional.json")
    with connect_database() as conn:
        homeowner_id_map = import_additional_homeowners(conn, homeowners) # type: ignore
        property_id_map = import_additional_properties(conn, properties, homeowner_id_map) # type: ignore
        import_additional_warranty_requests(conn, warranty_requests, property_id_map)
    return

if __name__ == "__main__":
    main()
        
        
    



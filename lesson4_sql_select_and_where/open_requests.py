from Applied_AI_Engineering_Lab_Pack.solutions.core import database
import sqlite3

def open_request(conn: sqlite3.Connection, property_id: int) -> tuple: # type: ignore
    """
    Retrieve open requests for a specific property from the database.

    Args:
        conn (sqlite3.Connection): The database connection object.
        property_id (int): The ID of the property to filter requests.   
        
    Returns:
        list: A list of tuples containing the open requests for the specified property.
    """
    
    cursor = conn.cursor()
    query = """
        SELECT * FROM requests
        WHERE property_id = ? AND status = 'open'
    """
    cursor.execute(query, (property_id,))
    open_requests = cursor.fetchall()
    return open_requests


with database() as conn:
    property_id = 1  # Example property ID to filter requests
    open_requests_list = open_request(conn, property_id)
    print(f"Open requests for property ID {property_id}:", open_requests_list) 
    

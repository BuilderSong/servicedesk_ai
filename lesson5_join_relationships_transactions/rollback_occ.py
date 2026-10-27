from lesson4_sql_select_and_where.postgresql import connect_database

def rollback_test(conn):
    try:
        cursor = conn.cursor()
        count = 0
        cursor.execute("""
                     INSERT INTO warranty_requests (property_id, category, description, status, assigned_to)
                     VALUES (%s, %s, %s, %s, %s)
                     """, (20, "plumbing", "right elevation hose bib is leaking", "open", "Steven"))
        count += cursor.rowcount
        cursor.execute(""" 
                        INSERT INTO warranty_requests (property_id, category, description, status, assigned_to)
                        VALUES (%s, %s, %s, %s, %s)
                        """, (80, "plumbing", "hot water tank is not heating up", "open", "Steven"))
        count += cursor.rowcount
        print(count)
        print("successed")
    except Exception as e:
        print(e)
        raise
    
    
def add_version(conn):
    cursor = conn.cursor()
    cursor.execute("""
    ALTER TABLE warranty_requests
    ADD COLUMN version INTEGER NOT NULL DEFAULT 1;
    """
    )
    print("added column version successed")

def update(conn, id):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE warranty_requests
            SET status = 'closed', version = version + 1
            WHERE id = %s AND version = 1;
            """, (id,)
            )
        if cursor.rowcount == 1:
            print("Update successful")
        else:
            print("No update: ID does not exist or version is no longer 1.")
    except Exception as e:
        print(e)
    
    
def main():
    with connect_database() as conn:
        update(conn, 103)
        update(conn, 103)
        
if __name__ == "__main__":
    main()
from lesson4_sql_select_and_where.postgresql import connect_database

def property_open_counts(conn):
    return conn.execute(
        """
        SELECT p.address, COUNT(w.id) AS open_counts
        FROM properties AS p
        LEFT JOIN warranty_requests as w
        ON p.id = w.property_id AND w.status = 'open'
        GROUP BY p.id
        ORDER BY p.id;            
        """).fetchall()
    
    
def main():
    with connect_database() as conn:
        results = property_open_counts(conn)
        for result in results:
            address, open_count = result
            print(f"{address} has {open_count} open requests")
        

if __name__ == "__main__":
    main()
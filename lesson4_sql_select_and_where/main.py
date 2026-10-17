from postgresql import connect_database


def main():
    with connect_database() as conn:
        database_name = conn.execute(
            "SELECT current_database();"
        ).fetchone()

        print("Connected to:", database_name[0]) # type: ignore

        columns = conn.execute(
            """
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position;
            """
        ).fetchall()

        for column in columns:
            print(column)


if __name__ == "__main__":
    main()
import psycopg2
import uuid

# Database connection parameters
db_params = {
    'dbname': 'generate_token',
    'user': 'huynh',
    'password': 'simplepassword',
    'host': 'localhost',
    'port': '5432',
}

def create_tickets(num_records):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    try:
        # Create a temporary table for bulk insertion
        cursor.execute('CREATE TEMP TABLE temp_tickets (id SERIAL PRIMARY KEY, token UUID)')

        # Generate UUIDs and insert into the temporary table
        tokens = [(str(uuid.uuid4()),) for _ in range(num_records)]
        cursor.executemany('INSERT INTO temp_tickets (token) VALUES (%s)', tokens)

        # Transfer data from the temporary table to the main table
        cursor.execute('INSERT INTO fix_regenerate_ticket (token) SELECT token FROM temp_tickets')

        conn.commit()
        print(f"{num_records} records with UUIDs have been created.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    num_records = 1000000
    create_tickets(num_records)

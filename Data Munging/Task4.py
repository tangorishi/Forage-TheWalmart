import csv
import sqlite3

def create_shipping_tables(cursor):
    # Create the 'shipments' table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipments (
            origin_warehouse TEXT,
            destination_store TEXT,
            product TEXT,
            on_time TEXT,
            product_quantity INTEGER,
            driver_identifier TEXT
        )
    """)

    # Create the 'shipment_info' table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipment_info (
            shipment_identifier TEXT,
            product TEXT,
            on_time TEXT,
            origin_warehouse TEXT,
            destination_store TEXT
        )
    """)

def insert_shipments_data(cursor):
    # Read data from 'shipments_data.csv' and insert it into the 'shipments' table
    with open('data/shipments_data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            origin_warehouse, destination_store, product, on_time, product_quantity, driver_identifier = row
            cursor.execute("INSERT INTO shipments (origin_warehouse, destination_store, product, on_time, product_quantity, driver_identifier) VALUES (?, ?, ?, ?, ?, ?)",
                           (origin_warehouse, destination_store, product, on_time, product_quantity, driver_identifier))

def insert_shipment_info(cursor):
    # Read data from 'shipment_info.csv' and 'shipments_data_2.csv'
    # Match the shipment identifiers and insert relevant data into the 'shipment_info' table
    with open('data/shipment_info.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        shipment_info_rows = [row for row in csv_reader]

    with open('data/shipments_data_2.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            shipment_identifier, product, on_time = row
            matching_rows = [r for r in shipment_info_rows if r[0] == shipment_identifier]
            if matching_rows:
                origin_warehouse, destination_store, driver_identifier = matching_rows[0][1], matching_rows[0][2], matching_rows[0][3]
                cursor.execute("INSERT INTO shipment_info (shipment_identifier, product, on_time, origin_warehouse, destination_store) VALUES (?, ?, ?, ?, ?)",
                               (shipment_identifier, product, on_time, origin_warehouse, destination_store))

if __name__ == "__main__":
    # Connect to the SQLite database
    conn = sqlite3.connect('shipment_database.db')
    cursor = conn.cursor()

    # Create the necessary tables in the database
    create_shipping_tables(cursor)

    # Insert data from 'shipments_data.csv' into the 'shipments' table
    insert_shipments_data(cursor)

    # Insert relevant data from 'shipment_info.csv' and 'shipments_data_2.csv' into the 'shipment_info' table
    insert_shipment_info(cursor)

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

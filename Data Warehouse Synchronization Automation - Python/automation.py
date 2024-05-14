import mysql.connector
import psycopg2
from datetime import datetime

# Connect to MySQL
mysql_connection = mysql.connector.connect(user='root', password='MTkxMDctaGFyc2hy', host='localhost', database='sales')
mysql_cursor = mysql_connection.cursor()

# Connect to PostgreSQL
postgres_connection = psycopg2.connect(database='postgres', user='postgres', password='MTE5MTAtaGFyc2hy', host='localhost', port='5432')
postgres_cursor = postgres_connection.cursor()

# Task 1 - Implement the function get_last_rowid()
def get_last_rowid():
    postgres_cursor.execute("SELECT MAX(rowid) FROM sales_data;")
    last_rowid = postgres_cursor.fetchone()[0]
    return last_rowid

# Task 2 - Implement the function get_latest_records()
def get_latest_records(rowid):
    mysql_cursor.execute("SELECT * FROM sales_data WHERE rowid > %s;", (rowid,))
    new_records = mysql_cursor.fetchall()
    return new_records

# Task 3 - Implement the function insert_records()
def insert_records(records):
    for record in records:
        # Check if the number of columns in the record matches the number of columns in the MySQL table
        if len(record) == 4:
            # If the record has 4 columns, insert default values for price and timestamp
            postgres_cursor.execute("INSERT INTO sales_data (rowid, product_id, customer_id, price, quantity, timestamp) VALUES (%s, %s, %s, 0.0, %s, current_timestamp);", record)
        else:
            # If the record has 5 columns, assume the price and timestamp values are provided and insert as is
            postgres_cursor.execute("INSERT INTO sales_data (rowid, product_id, customer_id, price, quantity, timestamp) VALUES (%s, %s, %s, %s, %s, %s);", record)
    postgres_connection.commit()

# Task 4 - Test the data synchronization
last_row_id = get_last_rowid()
print("Last row id on production data warehouse =", last_row_id)

new_records = get_latest_records(last_row_id)
print("New rows on staging data warehouse =", len(new_records))

# Print the latest records before insertion
print("Latest records to be inserted into production data warehouse:")
for record in new_records:
    print(record)

insert_records(new_records)
print("New rows inserted into production data warehouse =", len(new_records))

# Disconnect from MySQL and PostgreSQL
mysql_cursor.close()
mysql_connection.close()
postgres_cursor.close()
postgres_connection.close()

# End of program

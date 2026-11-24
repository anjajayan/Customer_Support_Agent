'''
This script contains functions to upload data to the database.
'''
import sqlite3
import pandas as pd

def upload_to_local_db():
    # Connect (creates the file if it doesn't exist)
    conn = sqlite3.connect("customer_support.db")

    # Load each CSV into its own table
    pd.read_csv("tables/customers.csv").to_sql("customers", conn, if_exists="replace", index=False)
    pd.read_csv("tables/orders.csv").to_sql("orders", conn, if_exists="replace", index=False)

    # Quick check
    # print("Customers table preview:")
    # print(pd.read_sql("SELECT * FROM customers LIMIT 5", conn))
    # print("Orders table preview:")
    # print(pd.read_sql("SELECT * FROM orders LIMIT 5", conn))
    
    print("Data upload complete.")
    conn.close()

upload_to_local_db()

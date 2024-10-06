import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import pooling

load_dotenv(dotenv_path='../.env')

dbconfig = {
    "database": "sql_ramen",
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "host": os.getenv('DB_HOST')
}

# Create a connection pool to avoid frequently connect and disconnect the database
connection_pool = pooling.MySQLConnectionPool(pool_name="mypool",
                                              pool_size=5,
                                              **dbconfig)

def get_db_connection():
    return connection_pool.get_connection()
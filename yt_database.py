import sqlite3
from sqlite3 import Error

import datetime

database_name = 'ytDatabase.db'
def create_connection():
    """ create a database connection to a SQLite database """
    file = 'ytDatabase.db'
    conn = None
    try:
        conn = sqlite3.connect(file)
        print('database created')
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_table(table_name: str):
    """create table if it doesn't exist"""
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    # clean table name
    table_name = table_name.replace('-','')

    # Creating a new SQLite table with 1 column
    c.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}\
        (id TEXT PRIMARY KEY, title TEXT, publishedat DATETIME, thumbnail TEXT, downloaded BOOLEAN DEFAULT 0)""")
    
    #commit the changes to db			
    conn.commit()
    #close the connection
    conn.close()

def new_table_entry(table:str, id:str,  title:str, publishedat:datetime, thumbnail:str):
    # Connecting to the database file
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    table = table.replace('-','')
    

    # insert id if it does not exist, ignore if exists
    sql = f"INSERT OR IGNORE INTO {table} VALUES(?,?,?,?,0)"
    c.execute(sql, ( id, title, publishedat, thumbnail,))

    conn.commit()
    conn.close()

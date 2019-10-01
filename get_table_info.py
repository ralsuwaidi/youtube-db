import sqlite3
import os

database_name = 'ytDatabase.db'

def get_database_tables():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    print('Connected to Database')

    sqlite_select_table = """SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"""
    c.execute(sqlite_select_table)
    table_list = c.fetchall()

    # SQL returns an array of size 2 for each table, we pick just one
    table_names=[]
    for item in table_list:
        table_names.append(item[0])
    conn.close()

    # list of table names
    return table_names


def get_database_rows(table_list):
    try:
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        print("Connected to SQLite")

        for table in table_list:
            c.execute("SELECT * from '{}' ".format(table))
            records = c.fetchall()
            print("Total rows are: ", len(records))
            print(records[0])
        conn.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (conn):
            conn.close()
            print("The SQLite connection closed")

def get_all_tables():
    table_rows = get_database_rows(get_database_tables())
    return table_rows
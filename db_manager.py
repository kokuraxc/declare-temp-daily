"""The Sqlite connector."""
import sqlite3

conn = sqlite3.connect('temperatures.db')
cur = conn.cursor()

table_name = 'temp_records'
dt_col_name = 'date_time'
temp_col_name = 'temperature'

query_create = '''CREATE TABLE IF NOT EXISTS temp_records
    ( date_time TEXT PRIMARY KEY,
    temperature REAL NOT NULL);'''
query_insert = '''INSERT INTO temp_records values (?, ?)'''

cur.execute(query_create)
cur.execute(query_insert, ('2020-10-26-AM', 36.5))
conn.commit()
conn.close()

"""The main logic with the database connector."""
import sqlite3
import datetime
import time
from auto_selenium import generate_temp, upload_temp
import random


def get_dt_str():
    """Get the date time string in the format of 2020-10-26-PM."""
    x = datetime.datetime.now()
    return x.strftime('%Y-%m-%d-%p')[:-1], x.strftime('%H%M')  # remove A/P[M]


def is_temp_recorded(db_cursor, dt_str):
    """Return True if the dt_str is recorded in the database."""
    db_cursor.execute(
        '''SELECT * FROM temp_records WHERE date_time = ?''', (dt_str,))
    row = db_cursor.fetchone()
    return False if row is None else True


def insert_record(db_conn, db_cursor, dt_str, temp):
    """Insert the temperature temp into the database."""
    query_insert = '''INSERT INTO temp_records values (?, ?)'''
    db_cursor.execute(query_insert, (dt_str, temp))
    db_conn.commit()
    print('Saved', dt_str, temp, 'to database.')


def is_time_permit(apm, time_str):
    """
    Check whether time permits proceeding.

    Disregard the random number,
    For AM: time_str should > 0820
    For PM: time_str should > 1220
    """
    rand_min = str(random.randrange(20, 40))
    if apm == 'A':
        rand_min = '08' + rand_min
    else:
        rand_min = '12' + rand_min

    if time_str < rand_min:
        return False
    return True


def update_web_and_db(db_conn, db_cur, dt_str, time_str):
    """Update the temp in website and database."""
    apm = dt_str[-1]
    if not is_time_permit(apm, time_str):
        return

    if not is_temp_recorded(db_cur, dt_str):
        temp = generate_temp(apm)
        upload_temp(apm, temp)
        insert_record(db_conn, db_cur, dt_str, temp)
    # else:
        # print(dt_str, 'already updated.')


conn = sqlite3.connect('temperatures.db')
cur = conn.cursor()

table_name = 'temp_records'
dt_col_name = 'date_time'
temp_col_name = 'temperature'

query_create = '''CREATE TABLE IF NOT EXISTS temp_records
    ( date_time TEXT PRIMARY KEY,
    temperature REAL NOT NULL);'''
cur.execute(query_create)
conn.commit()

while True:
    cur_dt_str, time_str = get_dt_str()
    if cur_dt_str.endswith('P'):
        am_dt_str = cur_dt_str.replace('P', 'A')
        update_web_and_db(conn, cur, am_dt_str, time_str)
    update_web_and_db(conn, cur, cur_dt_str, time_str)
    time.sleep(60)  # sleep for 1 min

conn.close()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------------------------------
try:
    import sys
    import time
    import datetime
    import logging
    import sqlite3
    import zz_wrapper_arduinoMF_v1 as serialarduino
except:
    print(sys.exc_info())

#----------------------------------------------------------------------------------------------------
logging.basicConfig(
filename='ll_log_tempsmokesensor.log',
format='%(asctime)s %(levelname)-2s %(message)s',
level=logging.INFO,
datefmt='%Y-%m-%d %H:%M:%S')

logging.info('#--- Script starting ---#')
arduino = serialarduino.InitComSerial()
#serialarduino.StatusComSerial(arduino)
serialarduino.SendComSerial(arduino,"cl:0")

sqlite3_db_file = 'ww_sqlite3_tempsmokesensor.db'
sqlite3_table_list = ['sensor','temp']
#----------------------------------------------------------------------------------------------------
def temp_analog_temp():
    print("Read analog started. CTRL+C to interrupt")
    try:
        while True:
            time.sleep(0.5)
            serialmsg = serialarduino.SendComSerial(arduino,"ra")
            serialarduino.SendComSerial(arduino,"wr:"+serialmsg.split('_')[1])
            insertVaribleIntoTable('sensor', datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), serialmsg.split('_')[1])
            time.sleep(0.5)
            serialmsg = serialarduino.SendComSerial(arduino,"gt")
            insertVaribleIntoTable('temp', datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), serialmsg.split('_')[1])

    except KeyboardInterrupt:
        print("\nRead analog interrupted")
        pass

#----------------------------------------------------------------------------------------------------
def close():
    serialarduino.SendComSerial(arduino,"cl:0") 
    serialarduino.CloseComSerial(arduino)
    logging.info('#--- Script ending ---#')

#----------------------------------------------------------------------------------------------------
def create_tables(sqlite3_table_list):
    try:
        sqliteConnection = sqlite3.connect(sqlite3_db_file)
        cursor = sqliteConnection.cursor()
        #print("Connected to SQLite")

        for table in sqlite3_table_list:
            sqlite_create = """CREATE TABLE IF NOT EXISTS {} (
                            date TEXT NOT NULL,
                            value TEXT
                            );""".format(table)

            cursor.execute(sqlite_create)
            sqliteConnection.commit()
            #print("Python Variables inserted successfully into SqliteDb_developers table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection is closed")

#----------------------------------------------------------------------------------------------------
def insertVaribleIntoTable(table, date, value):
    try:
        sqliteConnection = sqlite3.connect(sqlite3_db_file)
        cursor = sqliteConnection.cursor()
        #print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO {}
                          (date,value) 
                          VALUES (?, ?);""".format(table)

        data_tuple = (date, value)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        #print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection is closed")

#----------------------------------------------------------------------------------------------------
""" main """
if __name__ == '__main__':

    create_tables(sqlite3_table_list)
    temp_analog_temp()
    close()

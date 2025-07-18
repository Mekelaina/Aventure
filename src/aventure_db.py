import sqlite3
import typing
from pathlib import Path

from db_queries import *

# Gets the filepath to the database location
# in an OS independent way
def getDatabasePath() -> Path:
    cwd: Path = Path.cwd()
    dbdir: Path = cwd / 'database' / 'test.db'
    dbdir.resolve()
    return dbdir

# initializes the DB when bot launches.
# if DB doesnt exist, its created and initialized
# if DB does exist, then queries do nothing.
# no easy way to check if all tables exist,
# so always running is safest bet.
def initializeDB() -> None:
    print('Initializing DB')
    writeAllToDB([USERS_TABLE, ITEMS_TABLE])
    print('DB Initalization Complete')

# read from the DB and returns query result
# as a list of whatever was in the DB
# !!!should always be try/catched somewhere!!!
def readFromDB(query: str) -> list[typing.Any]:
    with sqlite3.connect(getDatabasePath()) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


# write to the DB. 
# if no error, the write was successful
# !!!should always be try/catched somewhere!!!
def writeToDB(insert: str) -> None:
    with sqlite3.connect(getDatabasePath()) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(insert)

# preform multiple writes to DB with one connection
# !!!should always be try/catched somewhere!!!
def writeAllToDB(insert: list[str]) -> None:
    with sqlite3.connect(getDatabasePath()) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        for i in insert:
            cursor.execute(i)

def debug():
    try:
        initializeDB()
    
    except sqlite3.Error as err:
        print('Error occurred -', err)
    
    # try:
    #     sqliteConnection = sqlite3.connect(q)
    #     cursor = sqliteConnection.cursor()
    #     print('DB Init')

    #     query = 'SELECT sqlite_version();'
    #     cursor.execute(query)

    #     result = cursor.fetchall()
    #     print('SQLite Version is {}'.format(result[0][0]))
        
    #     cursor.close()
    
    # except sqlite3.Error as error:
    #     print('Error occurred -', error)
    
    # finally:
    #     if sqliteConnection:
    #         sqliteConnection.close()
    #         print('SQLite Connection closed')



debug()
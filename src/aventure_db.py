import sqlite3
import typing
from pathlib import Path

from db_queries import *
from aventure_config import DATABASE

# Gets the filepath to the database location
# in an OS independent way
def getDatabasePath() -> Path:
    cwd: Path = Path.cwd()
    dbdir: Path = cwd / 'database' / DATABASE
    dbdir.resolve()
    return dbdir

# checks if expected database file exists
# returns true if yes, else false
def doesDBExist() -> bool:
    db_file = Path(getDatabasePath())
    if db_file.is_file():
        return True
    return False

# initializes the DB when bot launches.
# if DB doesnt exist, its created and initialized
# if DB does exist, then queries do nothing.
# no easy way to check if all tables exist,
# so always running is safest bet.
def initializeDB() -> bool:
    print('Initializing DB')
    
    if doesDBExist():
        #print("A")
        result, missing = verifyTablesPresent()
        if result == False:
            try:
                with sqlite3.connect(getDatabasePath()) as conn:
                    cursor = conn.cursor()
                    createTables(cursor, Tables.getValuesFromList(missing))
                   
            except sqlite3.Error as error:
                print('Error occurred -', error)
                return False
    else:
        try:
            with sqlite3.connect(getDatabasePath()) as conn:
                cursor = conn.cursor()
                createTables(cursor, Tables.getValues())
        except sqlite3.Error as error:
                print('Error occurred -', error)
                return False
    
    print('DB Initalization Complete')
    return True

# checks if the DB contains all Tables in the Tables enum
# true if yes, false if no
def verifyTablesPresent() -> tuple[bool, list[str]]:
    res = True
    missing = list()

    with sqlite3.connect(getDatabasePath()) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        tables = Tables.getNames()
        for table in tables:
            # this query only returns int 1 if table is present, int 0 otherwise
            cursor.execute(Checks.TABLE_EXISTS, (table,))
            x = cursor.fetchone()[0]
            if x == 0:
                res = False
                missing.append(table)
    return (res, missing)


# queries the DB and returns all results as a list
# depending on the number of results, memory could be an issues
# but given were only dealing with one player at a time
# it *shouldnt* be an issue
# !!!should always be try/catched somewhere!!!
def readAllFromDB(conn: sqlite3.Connection, cursor: sqlite3.Cursor, query: str, parameters=()) -> list[typing.Any]:
    cursor.execute(query)
    return cursor.fetchall()
    
def readFromDB(conn: sqlite3.Connection, cursor: sqlite3.Cursor, query: str, parameters=()) -> typing.Any:
    cursor.execute(query, parameters)
    return cursor.fetchone()


# write to the DB. 
# if no error, the write was successful
# !!!should always be try/catched somewhere!!!
def writeToDB(conn: sqlite3.Connection, cursor: sqlite3.Connection, statement: str, parameters) -> None:
        cursor.execute(statement, parameters)
        conn.commit()

#only used to create tables
def createTables(cursor: sqlite3.Cursor, tables: list[str]) -> None:
    for i in tables:
            cursor.execute(i)

#retruns true if entry with given id exists in given table
#false otherwise
#USERS is if you are checking the USERS table
def checkEntry(cursor: sqlite3.Cursor, table: str, id: int) -> bool:
    match table:
        case Tables.USERS.name:
            cursor.execute(Checks.ENTRY_USERS_EXISTS, (id,))
        case Tables.PLAYER_COMBAT:
            cursor.execute(Checks.ENTRY_PLAYER_COMBAT_EXISTS, (id,))
        case Tables.PLAYER_DUNGEON:
            cursor.execute(Checks.ENTRY_PLAYER_DUNGEON_EXISTS, (id,))
        case Tables.PLAYER_EQUIPMENT:
            cursor.execute(Checks.ENTRY_PLAYER_EQUIPMENT_EXISTS, (id,))
        case Tables.PLAYER_INFO:
            cursor.execute(Checks.ENTRY_PLAYER_INFO_EXISTS, (id,))
        case Tables.PLAYER_STATS:
            cursor.execute(Checks.ENTRY_PLAYER_STATS_EXISTS, (id,))
    
    res = cursor.fetchone()[0]
    if res == 1:
        return True
    else:
        return False



def debug():
   pass
    # initializeDB()
    # try:
    #     with sqlite3.connect(getDatabasePath()) as conn:
    #         cursor = conn.cursor()
    #         writeToDB(conn, cursor, Inserts.USERS, (123,))
    #         writeToDB(conn, cursor, Inserts.USERS, (456,))
    #         writeToDB(conn, cursor, Inserts.USERS, (789,))
    #         print("ee")
    #         if checkEntry(cursor, Tables.USERS.name, 123):
    #             print("aba")
    #         else:
    #             print('boo')
            
    # except sqlite3.Error as error:
    #     print('Error occurred -', error)

    

#debug()
import sqlite3
import typing
from pathlib import Path

from db_queries import Tables

# Gets the filepath to the database location
# in an OS independent way
def getDatabasePath() -> Path:
    cwd: Path = Path.cwd()
    dbdir: Path = cwd / 'database' / 'test.db'
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
def initializeDB() -> None:
    print('Initializing DB')
    
    if doesDBExist():
        print("A")
        result, missing = verifyTablesPresent()
        if result == False:
            try:
                writeAllToDB(Tables.getValuesFromList(missing))
                # TODO populate missing tables if applicable    
            except sqlite3.Error as error:
                print('Error occurred -', error)
    else:
        try:
            writeAllToDB(Tables.getValues())
        except sqlite3.Error as error:
                print('Error occurred -', error)
    
    print('DB Initalization Complete')

# checks if the DB contains all Tables in the Tables enum
# true if yes, false if no
def verifyTablesPresent() -> tuple[bool, list[str]]:
    res = True
    missing = list()

    with sqlite3.connect(getDatabasePath()) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        for table in Tables.getNames():
            # this query only returns int 1 if table is present, int 0 otherwise
            cursor.execute(f'SELECT EXISTS(SELECT 1 FROM sqlite_master WHERE type="table" AND name="{table}");')
            if cursor.fetchone()[0] == 0:
                res = False
                missing.append(table)
    return (res, missing)


# queries the DB and returns all results as a list
# depending on the number of results, memory could be an issues
# but given were only dealing with one player at a time
# it *shouldnt* be an issue
# !!!should always be try/catched somewhere!!!
def readAllFromDB(query: str, parameters=()) -> list[typing.Any]:
    with sqlite3.connect(getDatabasePath()) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
def readFromDB(query: str, parameters=()) -> typing.Any:
    with sqlite3.connect(getDatabasePath()) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchone()


# write to the DB. 
# if no error, the write was successful
# !!!should always be try/catched somewhere!!!
def writeToDB(insert: str, parameters=()) -> None:
    with sqlite3.connect(getDatabasePath()) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(insert, parameters)

# preform multiple writes to DB with one connection
# !!!should always be try/catched somewhere!!!
def writeAllToDB(insert: list[str]) -> None:
    with sqlite3.connect(getDatabasePath()) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        for i in insert:
            cursor.execute(i)


def debug():
   
    initializeDB()
    try:

        writeToDB(f'INSERT INTO "USERS" VALUES(null,{181})')
        res = readAllFromDB(f'SELECT * FROM "USERS"')
        print(res)
    except sqlite3.Error as error:
        print('Error occurred -', error)

    # sqliteConnection: sqlite3.Connection
    # try:
    #     sqliteConnection = sqlite3.connect(getDatabasePath())
    #     cursor = sqliteConnection.cursor()
    #     print('DB Init')

    #     testID: int = 180
    #     print(Tables.getNames())
    #     query = '''INSERT INTO 'USERS' VALUES(?)'''
    #     cursor.execute(query, testID)

    #     result = cursor.fetchone()
    #     print(type(result[0]))
    #     print(result)
    #     print('SQLite Version is {}'.format(result[0][0]))
        
    #     cursor.close()
    # except sqlite3.Error as error:
    #     print('Error occurred -', error)
    # finally:
    #     if sqliteConnection:
    #         sqliteConnection.close()
    #         print('SQLite Connection closed')

debug()
import aiosqlite 
import typing
from aiopath import Path

from db_queries import *
from aventure_config import DATABASE
from aventure_player import Player, playerData, statsData, equipmentData
import aventure_map as map
import aventure_enemy as enemy

# Gets the filepath to the database location
# in an OS independent way
async def getDatabasePath() -> Path:
    cwd: Path = await Path.cwd()
    dbdir: Path = cwd / 'database' / DATABASE
    await dbdir.resolve()
    return dbdir

# checks if expected database file exists
# returns true if yes, else false
async def _doesDBExist() -> bool:
    #print('A')
    db_file: Path = await getDatabasePath()
    #print('B')
    if await db_file.is_file():
        #print('C')
        return True
    return False

# initializes the DB when bot launches.
# if DB doesnt exist, its created and initialized
# if DB does exist, then queries do nothing.
# no easy way to check if all tables exist,
# so always running is safest bet.
async def initializeDB() -> bool:
    print('Initializing DB')
    
    if await _doesDBExist():
        
        result, missing = await _verifyTablesPresent()
        print('ee')
        if result == False:
            try:
                async with aiosqlite.connect(await getDatabasePath()) as conn:
                    cursor: aiosqlite.Connection = await  conn.cursor()
                    await _createTables(cursor, Tables.getValuesFromList(missing))
                   
            except aiosqlite.Error as error:
                print('Error occurred -', error)
                return False
    else:
        try:
            
            async with aiosqlite.connect(await getDatabasePath()) as conn:
                
                cursor = await conn.cursor()
                await _createTables(cursor, Tables.getValues())
        except aiosqlite.Error as error:
                print('Error occurred -', error)
                return False
    
    print('DB Initalization Complete')
    return True

async def pls(s: list[str]):
    for x in s:
        yield x

# checks if the DB contains all Tables in the Tables enum
# true if yes, false if no
async def _verifyTablesPresent() -> tuple[bool, list[str]]:
    res = True
    missing = []
    
    async with aiosqlite.connect(await getDatabasePath()) as conn:
        
        cursor: aiosqlite.Cursor = await conn.cursor()
       
        tables = await Tables.getNames()
        #remove loop
        async for table in pls(tables):
            # this query only returns int 1 if table is present, int 0 otherwise
            await cursor.execute(Checks.TABLE_EXISTS, (table,))
            print('e')
            x = await cursor.fetchone()
            print('f')
            x = x[0]
            if x == 0:
                res = False
                await missing.append(table)
    return (res, missing)


# queries the DB and returns all results as a list
# depending on the number of results, memory could be an issues
# but given were only dealing with one player at a time
# it *shouldnt* be an issue
# !!!should always be try/catched somewhere!!!
async def _readAllFromDB( cursor: aiosqlite.Cursor, query: str, parameters=()) -> list[typing.Any]:
    await cursor.execute(query)
    return await cursor.fetchall()
    
async def _readFromDB( cursor: aiosqlite.Cursor, query: str, parameters=()) -> typing.Any:
    await cursor.execute(query, parameters)
    return await cursor.fetchone()


# write to the DB. 
# if no error, the write was successful
# !!!should always be try/catched somewhere!!!
async def _writeToDB(conn: aiosqlite.Connection, cursor: aiosqlite.Connection, statement: str, parameters) -> None:
        await cursor.execute(statement, parameters)
        await conn.commit()

#only used to create tables
async def _createTables(cursor: aiosqlite.Cursor, tables: list[str]) -> None:
    for i in tables:
            await cursor.execute(i)

#retruns true if entry with given id exists in given table
#false otherwise
#USERS is if you are checking the USERS table
async def _checkEntry(cursor: aiosqlite.Cursor, table: str, id: int) -> bool:
    match table:
        case Tables.USERS.name:
            await cursor.execute(Checks.ENTRY_USERS_EXISTS, (id,))
        case Tables.PLAYER_COMBAT.name:
            await cursor.execute(Checks.ENTRY_PLAYER_COMBAT_EXISTS, (id,))
        case Tables.PLAYER_DUNGEON.name:
            await cursor.execute(Checks.ENTRY_PLAYER_DUNGEON_EXISTS, (id,))
        case Tables.PLAYER_EQUIPMENT.name:
            await cursor.execute(Checks.ENTRY_PLAYER_EQUIPMENT_EXISTS, (id,))
        case Tables.PLAYER_INFO.name:
            await cursor.execute(Checks.ENTRY_PLAYER_INFO_EXISTS, (id,))
        case Tables.PLAYER_STATS.name:
            await cursor.execute(Checks.ENTRY_PLAYER_STATS_EXISTS, (id,))
    
    res = await cursor.fetchone()[0]
    if res == 1:
        return True
    else:
        return False

async def findUser(cursor: aiosqlite.Cursor, discord_id: int) -> None:
    #print("egg")
    if await _checkEntry(cursor, Tables.USERS.name, discord_id):
        return True
    else:
        return False

async def newUser(conn: aiosqlite.Connection, cursor: aiosqlite.Cursor, discord_id: int, 
                  p: Player, m: map.Map, e: enemy.GameEnemy):
    await _writeToDB(conn, cursor, Inserts.USERS, (discord_id,))
    #pData = p.save()
    #print(pData)
    

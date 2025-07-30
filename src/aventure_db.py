import aiosqlite 
import typing
import asyncio
from aiopath import Path

from db_queries import *
from aventure_config import DATABASE
from aventure_player import Player, playerData, statsData, equipmentData, GameState
from aventure_map import Map
from aventure_enemy import GameEnemy

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
                
                await _createTables(cursor, await Tables.getValues())
                
        except aiosqlite.Error as error:
                print('Error occurred -', error)
                return False
    
    print('DB Initalization Complete')
    return True


# checks if the DB contains all Tables in the Tables enum
# true if yes, false if no
async def _verifyTablesPresent() -> tuple[bool, list[str]]:
    res = True
    missing = []
    
    async with aiosqlite.connect(await getDatabasePath()) as conn:
        
        cursor: aiosqlite.Cursor = await conn.cursor()
       
        #loops that call async code dont work.
        
        tables = await Tables.getNames()
        for table in tables:
            # this query only returns int 1 if table is present, int 0 otherwise
            await cursor.execute(Checks.TABLE_EXISTS, (table,))
            
            x = await cursor.fetchone()
            
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

async def _createTable(cursor: aiosqlite.Cursor, table: str) -> None:
    await cursor.execute(table)

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
    
    res = await cursor.fetchone()
    
    res = res[0]
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

async def loadUser(conn: aiosqlite.Connection, cursor: aiosqlite.Cursor, discord_id: int, 
                  p: Player, m: Map, e: GameEnemy) -> int:
    user = await _readFromDB(cursor, Gets.USERS_ROW, (discord_id,))
    user_id = user[0]
    choice = await _readFromDB(cursor, Gets.PLAYER_CHOICE_ROW, (user_id,))
    combat = await _readFromDB(cursor, Gets.PLAYER_COMBAT_ROW, (user_id,))
    dungeon = await _readFromDB(cursor, Gets.PLAYER_DUNGEON_ROW, (user_id,))
    #print('2')
    info = await _readFromDB(cursor, Gets.PLAYER_INFO_ROW, (user_id,))
    stats = await _readFromDB(cursor, Gets.PLAYER_STATS_ROW, (user_id,))
    eq = await _readFromDB(cursor, Gets.PLAYER_EQUIPMENT_ROW, (user_id,))
    #parse and assemble player data from tables
    temp = list(info)
    state = temp[2]
    pData = tuple(temp[3:])
    
    temp = list(stats)
    pStats = tuple(temp[2:])
    temp = list(eq)
    
    
    pi = temp.pop()
    ri = temp.pop()
    pEq = tuple(temp[2:])
    temp = list(choice)
    pChoice = tuple(temp[2:])
    #print('LOAD: ', pData)
    await p.load([state, pData, pStats, pEq, ri, pi, pChoice])
   



    temp = list(combat)
    temp = temp[2:]
  
    inCombat = temp[0]
    eData = temp[1]
    await e.deserialize(eData)
   
    
    temp = list(dungeon)
    dungeon = dungeon[2:]
    await m.deserialize(tuple(dungeon))
    #task3 = asyncio.create_task(m.deserialize(tuple(dungeon)))
    # await task1
   
    # await task2

    # await task3
    #print("1")
    
    return user_id

    
async def saveUser(conn: aiosqlite.Connection, cursor: aiosqlite.Cursor, discord_id: int, 
                  p: Player, m: Map, e: GameEnemy):
    user = await _readFromDB(cursor, Gets.USERS_ROW, (discord_id,))
    user_id = user[0]
    
    pData = await p.save()
    mData = await m.serialize()
    eData = await e.serialize()

    await _writeToDB(conn, cursor, Updates.PLAYER_DUNGEON, (mData[0], mData[1], user_id))

    in_combat = True if p.state == GameState.RUN_COMBAT else False
    await _writeToDB(conn, cursor, Updates.PLAYER_COMBAT, (in_combat, eData, user_id))
    
    state = pData.pop(0)
    temp: tuple = pData.pop(0)
    #print('SAVE: ', temp)
    temp = (state,) + temp + (user_id,)
    await _writeToDB(conn, cursor, Updates.PLAYER_INFO, temp)
    
    temp: tuple  = pData.pop(0)
    temp = temp + (user_id,) 
    await _writeToDB(conn, cursor, Updates.PLAYER_STATS, temp)
    
    temp: tuple = pData.pop(0)
    ri = pData.pop(0)
    pi = pData.pop(0)
    temp = temp + (ri, pi) + (user_id,)
    await _writeToDB(conn, cursor, Updates.PLAYER_EQUIPMENT, temp)
    
    temp = pData.pop(0)
    temp = temp + (user_id,)
    await _writeToDB(conn, cursor, Updates.PLAYER_CHOICE, temp)
async def deleteUser(conn: aiosqlite.Connection, cursor: aiosqlite.Cursor, discord_id: int, user_id: int):
    await _writeToDB(conn, cursor, Deletes.USERS, (discord_id,))
    await _writeToDB(conn, cursor, Deletes.PLAYER_CHOICE, (user_id,))
    await _writeToDB(conn, cursor, Deletes.PLAYER_COMBAT, (user_id,))
    await _writeToDB(conn, cursor, Deletes.PLAYER_DUNGEON, (user_id,))
    await _writeToDB(conn, cursor, Deletes.PLAYER_EQUIPMENT, (user_id,))
    await _writeToDB(conn, cursor, Deletes.PLAYER_INFO, (user_id,))
    await _writeToDB(conn, cursor, Deletes.PLAYER_STATS, (user_id,))
    
    

async def newUser(conn: aiosqlite.Connection, cursor: aiosqlite.Cursor, discord_id: int, 
                  p: Player, m: Map, e: GameEnemy):
    #print('Ah')
    await _writeToDB(conn, cursor, Inserts.USERS, (discord_id,))
    user = await _readFromDB(cursor, Gets.USERS_ROW, (discord_id,))
    user_id = user[0]
    pData = await p.save()
    mData = await m.serialize()
    eData = await e.serialize()

    
    await _writeToDB(conn, cursor, Inserts.PLAYER_COMBAT, (user_id, 0, eData))
    await _writeToDB(conn, cursor, Inserts.PLAYER_DUNGEON, (user_id, mData[0], mData[1]))
    
    state = pData.pop(0)
    temp: tuple = pData.pop(0)
    temp = (user_id,) + (state,) + temp
    #print(temp)
    await _writeToDB(conn, cursor, Inserts.PLAYER_INFO, temp)
    
    temp: tuple = pData.pop(0)
    temp = (user_id,) + temp
    await _writeToDB(conn, cursor, Inserts.PLAYER_STATS, temp)

    temp: tuple = pData.pop(0)
    ri = pData.pop(0)
    pi = pData.pop(0)
    temp = (user_id,) + temp + (ri, pi)
    await _writeToDB(conn, cursor, Inserts.PLAYER_EQUIPMENT, temp)

    temp: tuple = pData.pop(0)
    temp = (user_id,) + temp
    await _writeToDB(conn, cursor, Inserts.PLAYER_CHOICE, temp)
    

    

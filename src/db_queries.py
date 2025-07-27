
from enum import StrEnum
from multiprocessing import pool


# All the queries regularly made as constants

# === Table Constructors === #

# extedning base enum class so all of our enums
# can use the shared functions
class ExtEnum(StrEnum):

    # gets all enum values as a list
    @classmethod
    async def getValues(cls) -> list[str]:
        rtn = []

        for i in cls:
            rtn.append(i.value)
        return rtn
    
    # gets all enum names as a list
    @classmethod
    async def getNames(cls) -> list[str]:
        rtn = []
        
        for i in cls:
            rtn.append(i.name)
        return  rtn #list(pool.Pool.map_async(lambda c: c.name, cls))
    
    @classmethod
    async def getValuesFromList(cls, names: list[str]) -> list[str]:
        buff = []
        for i in cls:
            if i.name in names:
                buff.append(i.value)
        return buff
    

class Tables(ExtEnum):

    USERS = '''CREATE TABLE IF NOT EXISTS "USERS" (
	    "USER_ID"	INTEGER NOT NULL UNIQUE,
	    "DISCORD_ID"	INTEGER NOT NULL UNIQUE COLLATE BINARY,
	    PRIMARY KEY("USER_ID" AUTOINCREMENT)
    ) STRICT;'''

    PLAYER_COMBAT = '''CREATE TABLE "PLAYER_COMBAT" (
        "COMBAT_ID"	INTEGER NOT NULL UNIQUE,
        "USER"	INTEGER NOT NULL UNIQUE COLLATE BINARY,
        "IN_COMBAT"	INTEGER NOT NULL DEFAULT 0 CHECK("IN_COMBAT" == 0 OR "IN_COMBAT" == 1),
        "ENEMY"	BLOB NOT NULL DEFAULT 0,
        PRIMARY KEY("COMBAT_ID" AUTOINCREMENT),
        FOREIGN KEY("USER") REFERENCES "USERS"("USER_ID") ON DELETE CASCADE
    ) STRICT;'''

    PLAYER_DUNGEON = '''CREATE TABLE "PLAYER_DUNGEON" (
        "DUNGEON_ID"	INTEGER NOT NULL UNIQUE,
        "USER"	INTEGER NOT NULL UNIQUE,
        "MAP"	INTEGER NOT NULL,
        "ROOMS"	BLOB NOT NULL DEFAULT 0,
        PRIMARY KEY("DUNGEON_ID" AUTOINCREMENT),
        FOREIGN KEY("USER") REFERENCES "USERS"("USER_ID") ON DELETE CASCADE
    ) STRICT;'''

    PLAYER_EQUIPMENT = '''CREATE TABLE "PLAYER_EQUIPMENT" (
        "EQUIPMENT_ID"	INTEGER NOT NULL UNIQUE,
        "USER"	INTEGER NOT NULL UNIQUE COLLATE BINARY,
        "KEY"	INTEGER NOT NULL DEFAULT 0 CHECK("KEY" == 0 OR "KEY" == 1),
        "WEAPON"	INTEGER NOT NULL DEFAULT 0,
        "ARMOR"	INTEGER NOT NULL DEFAULT 0,
        "OFFHAND"	INTEGER NOT NULL DEFAULT 0,
        "CON1_ITEM"	INTEGER NOT NULL DEFAULT 0,
        "CON1_COUNT"	INTEGER NOT NULL DEFAULT 0,
        "CON2_ITEM"	INTEGER NOT NULL DEFAULT 0,
        "CON2_COUNT"	INTEGER NOT NULL DEFAULT 0,
        "RUN_INVENTORY"	BLOB NOT NULL DEFAULT 0,
        "POST_INVENTORY"	BLOB NOT NULL DEFAULT 0,
        PRIMARY KEY("EQUIPMENT_ID" AUTOINCREMENT),
        FOREIGN KEY("USER") REFERENCES "USERS"("USER_ID") ON DELETE CASCADE,
        CHECK("KEY" == 0 | "KEY" == 1)
    ) STRICT;'''

    PLAYER_INFO = '''CREATE TABLE "PLAYER_INFO" (
        "INFO_ID"	INTEGER NOT NULL UNIQUE,
        "USER"	INTEGER NOT NULL UNIQUE COLLATE BINARY,
        "GAME_STATE"	INTEGER NOT NULL DEFAULT 0 CHECK("GAME_STATE" >= 0 AND "GAME_STATE" < 5),
        "LEVEL"	INTEGER NOT NULL DEFAULT 1,
        "HEALTH_MAX"	INTEGER NOT NULL DEFAULT 0,
        "HEALTH_CURRENT"	INTEGER NOT NULL DEFAULT 0,
        "ATTACK"	INTEGER NOT NULL DEFAULT 0,
        "DEFENSE"	INTEGER NOT NULL DEFAULT 0,
        "EXP"	INTEGER NOT NULL DEFAULT 0,
        "GOLD"	INTEGER NOT NULL DEFAULT 0,
        "ALIVE"	INTEGER NOT NULL DEFAULT 1 CHECK("ALIVE" == 0 OR "ALIVE" == 1),
        "MAP"	INTEGER NOT NULL DEFAULT -1,
        "ROOM"	INTEGER NOT NULL DEFAULT -1,
        "LAST_MOVE"	INTEGER NOT NULL DEFAULT 0 CHECK("LAST_MOVE" >= 0 AND "LAST_MOVE" < 4),
        "HAS_MOVED" INTEGER NOT NULL DEFAULT 0 CHECK("HAS_MOVED" == 0 OR "HAS_MOVED" == 1),
        PRIMARY KEY("INFO_ID" AUTOINCREMENT),
        FOREIGN KEY("USER") REFERENCES "USERS"("USER_ID") ON DELETE CASCADE
    ) STRICT;'''

    PLAYER_STATS = '''CREATE TABLE "PLAYER_STATS" (
        "STATS_ID"	INTEGER NOT NULL UNIQUE,
        "USER"	INTEGER NOT NULL UNIQUE COLLATE BINARY,
        "DUNGEONS_CLEARED"	INTEGER NOT NULL DEFAULT 0,
        "ENEMIES_KILLED"	INTEGER NOT NULL DEFAULT 0,
        "DEATHS"	INTEGER NOT NULL DEFAULT 0,
        "TOTAL_GOLD"	INTEGER NOT NULL DEFAULT 0,
        "TOTAL_ITEMS"	INTEGER NOT NULL DEFAULT 0,
        "MESSAGES_SENT"	INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY("STATS_ID" AUTOINCREMENT),
        FOREIGN KEY("USER") REFERENCES "USERS"("USER_ID") ON DELETE CASCADE
    ) STRICT;'''

class Checks(ExtEnum):
    TABLE_EXISTS = 'SELECT EXISTS(SELECT 1 FROM sqlite_master WHERE type="table" AND name=?);'

    ENTRY_USERS_EXISTS = 'SELECT EXISTS(SELECT 1 FROM USERS WHERE DISCORD_ID = ?);'

    ENTRY_PLAYER_COMBAT_EXISTS = 'SELECT EXISTS(SELECT 1 FROM PLAYER_COMBAT WHERE USER = ?);'

    ENTRY_PLAYER_DUNGEON_EXISTS = 'SELECT EXISTS(SELECT 1 FROM PLAYER_DUNGEON WHERE USER = ?);'

    ENTRY_PLAYER_EQUIPMENT_EXISTS = 'SELECT EXISTS(SELECT 1 FROM PLAYER_EQUIPMENT WHERE USER = ?);'

    ENTRY_PLAYER_INFO_EXISTS = 'SELECT EXISTS(SELECT 1 FROM PLAYER_INFO WHERE USER = ?);'

    ENTRY_PLAYER_STATS_EXISTS = 'SELECT EXISTS(SELECT 1 FROM PLAYER_STATS WHERE USER = ?);'

class Gets(ExtEnum):
    ROW = 'SELECT * FROM ? WHERE ? = ?;'
    USERS_ROW = 'SELECT * FROM USERS WHERE DISCORD_ID = ?;'
    PLAYER_COMBAT_ROW = 'SELECT * FROM PLAYER_COMBAT WHERE USER = ?;'
    PLAYER_DUNGEON_ROW = 'SELECT * FROM PLAYER_DUNGEON WHERE USER = ?;'
    PLAYER_EQUIPMENT_ROW = 'SELECT * FROM PLAYER_EQUIPMENT WHERE USER = ?;'
    PLAYER_INFO_ROW = 'SELECT * FROM PLAYER_INFO WHERE USER = ?;'
    PLAYER_STATS_ROW = 'SELECT * FROM PLAYER_STATS WHERE USER = ?;'

class Inserts(ExtEnum):
    USERS = 'INSERT INTO "USERS" (USER_ID, DISCORD_ID) VALUES(NULL, ?);'

    PLAYER_COMBAT = '''INSERT INTO "PLAYER_COMBAT" (
        COMBAT_ID, USER, IN_COMBAT, ENEMY) 
        VALUES (NULL, ?, ?, ?);'''
    
    PLAYER_DUNGEON = '''INSERT INTO "PLAYER_DUNGEON" (
        DUNGEON_ID, USER, MAP, ROOMS)
        VALUES (NULL, ?, ?, ?);'''
    
    PLAYER_EQUIPMENT = '''INSERT INTO "PLAYER_EQUIPMENT" (
        EQUIPMENT_ID, USER, KEY, WEAPON, ARMOR, OFFHAND,
        CON1_ITEM, CON1_COUNT, CON2_ITEM, CON2_COUNT,
        RUN_INVENTORY, POST_INVENTORY)
        VALUES (NULL, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, 
        ?, ?);'''
    
    PLAYER_INFO = '''INSERT INTO "PLAYER_INFO" (
        INFO_ID, USER, GAME_STATE, LEVEL, HEALTH_MAX, 
        HEALTH_CURRENT, ATTACK, DEFENSE, EXP, 
        GOLD, ALIVE, MAP, ROOM,
        LAST_MOVE, HAS_MOVED) VALUES (
        NULL, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?);'''
    
    PLAYER_STATS = '''INSERT INTO "PLAYER_STATS" (
        STATS_ID, USER, DUNGEONS_CLEARED,
        ENEMIES_KILLED, DEATHS, TOTAL_GOLD,
        TOTAL_ITEMS, MESSAGES_SENT) VALUES (
        NULL, ?, ?,
        ?, ?, ?,
        ?, ?);'''
    
class Updates(ExtEnum):
    PLAYER_COMBAT = '''UPDATE "PLAYER_COMBAT"
        SET IN_COMBAT = ?,
            ENEMY = ?
        WHERE USER == ?;'''
    
    PLAYER_DUNGEON = '''UPDATE "PLAYER_DUNGEON"
        SET MAP = ?,
            ROOMS = ?
        WHERE USER == ?;'''
    
    PLAYER_EQUIPMENT = '''UPDATE "PLAYER_EQUIPMENT"
        SET KEY = ?,
            WEAPON = ?,
            ARMOR = ?,
            OFFHAND = ?,
            CON1_ITEM = ?,
            CON1_COUNT = ?,
            CON2_ITEM = ?,
            CON2_COUNT = ?,
            RUN_INVENTORY = ?,
            POST_INVENTORY = ?
        WHERE USER == ?;'''
    
    PLAYER_INFO = '''UPDATE "PLAYER_INFO"
        SET GAME_STATE = ?,
            LEVEL = ?,
            HEALTH_MAX = ?,
            HEALTH_CURRENT = ?,
            ATTACK = ?,
            DEFENSE = ?,
            EXP = ?,
            GOLD = ?,
            ALIVE = ?,
            MAP = ?,
            ROOM = ?,
            LAST_MOVE = ?,
            HAS_MOVED = ?
        WHERE USER == ?;'''
    
    PLAYER_STATS = '''UPDATE "PLAYER_STATS"
        SET DUNGEONS_CLEARED = ?,
            ENEMIES_KILLED = ?,
            DEATHS = ?,
            TOTAL_GOLD = ?,
            TOTAL_ITEMS = ?,
            MESSAGES_SENT = ?
        WHERE USER == ?;'''

class Deletes(ExtEnum):

    USERS = '''DELETE FROM USERS WHERE DISCORD_ID == ?;'''

    PLAYER_COMBAT = '''DELETE FROM PLAYER_COMBAT WHERE USER == ?;'''

    PLAYER_DUNGEON = '''DELETE FROM PLAYER_DUNGEON WHERE USER == ?;'''

    PLAYER_EQUIPMENT = '''DELETE FROM PLAYER_EQUIPMENT WHERE USER == ?;'''

    PLAYER_INFO = '''DELETE FROM PLAYER_INFO WHERE USER == ?;'''

    PLAYER_STATS = '''DELETE FROM PLAYER_STATS WHERE USER == ?;'''

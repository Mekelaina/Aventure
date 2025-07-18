
from enum import Enum


# All the queries regularly made as constants

# === Table Constructors === #

# extedning base enum class so all of our enums
# can use the shared functions
class ExtEnum(Enum):

    # gets all enum values as a list
    @classmethod
    def getValues(self) -> list[str]:
        return list(map(lambda c: c.value, self))
    
    # gets all enum names as a list
    @classmethod
    def getNames(self) -> list[str]:
        return list(map(lambda c: c.name, self))
    

class Tables(ExtEnum):

    USERS = '''CREATE TABLE IF NOT EXISTS "USERS" (
	    "USER_ID"	INTEGER NOT NULL UNIQUE,
	    "DISCORD_ID"	INTEGER NOT NULL UNIQUE COLLATE BINARY,
	    PRIMARY KEY("USER_ID" AUTOINCREMENT)
    ) STRICT;'''

    ITEMS = '''CREATE TABLE IF NOT EXISTS "ITEMS" (
        "ITEM_ID"	INTEGER NOT NULL UNIQUE COLLATE BINARY,
        "NAME"	TEXT NOT NULL DEFAULT '',
        "DESCRIPTION"	TEXT NOT NULL DEFAULT '',
        "VALUE"	INTEGER NOT NULL DEFAULT 0,
        "MOD"	INTEGER NOT NULL DEFAULT 0,
        "USECASE"	INTEGER NOT NULL DEFAULT 0 CHECK("USECASE" >= 0 AND "USECASE" < 5),
        "EQUIPABLE"	INTEGER NOT NULL DEFAULT 0 CHECK("EQUIPABLE" >= 0 AND "EQUIPABLE" < 5),
        PRIMARY KEY("ITEM_ID" AUTOINCREMENT)
    ) STRICT;'''
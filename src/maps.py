from enum import IntEnum
from aventure_map import *
from ascii_bulder import buildRoom
from enemies import EnemyID
from items import ItemID

class MapID(IntEnum):
    TEST_MAP_EMPTY = 0
    TEST_MAP_FIGHT = 1
    MAIN_MAP = 2

GAME_MAPS: dict[MapID , Map] = {
    MapID.TEST_MAP_EMPTY : Map(MapID.TEST_MAP_EMPTY, rooms=[
        Room(id=0, layout={
            Direction.NORTH : Door(False, 1),
            Direction.EAST : Door(True, 2),
            Direction.SOUTH : Door(False, 3),
            Direction.WEST : Door(True, 4)
            }),
        Room(id=1, layout={
            Direction.NORTH : Door(False, -1),
            Direction.EAST : Door(False, -1),
            Direction.SOUTH : Door(True, 0),
            Direction.WEST : Door(False, -1)
        }),
        Room(id=2, layout={
            Direction.NORTH : Door(False, -1),
            Direction.EAST : Door(False, -1),
            Direction.SOUTH : Door(False, -1),
            Direction.WEST : Door(True, 0)
        }),
        Room(id=3, layout={
            Direction.NORTH : Door(True, 0),
            Direction.EAST : Door(False, -1),
            Direction.SOUTH : Door(False, -1),
            Direction.WEST : Door(False, -1)
        }),
        Room(id=4, layout={
            Direction.NORTH : Door(False, -1),
            Direction.EAST : Door(True, 0),
            Direction.SOUTH : Door(False, -1),
            Direction.WEST : Door(False, -1)
        })
    ]),
    MapID.TEST_MAP_FIGHT : Map(MapID.TEST_MAP_FIGHT, rooms=[
        Room(id=0, layout={
            Direction.NORTH : Door(True, 1),
            Direction.EAST : Door(True, 2),
            Direction.SOUTH : Door(False, 3),
            Direction.WEST : Door(True, 4)
            }),
        Room(id=1, layout={
            Direction.NORTH : Door(False, -1),
            Direction.EAST : Door(False, -1),
            Direction.SOUTH : Door(True, 0),
            Direction.WEST : Door(False, -1)
        }, loot=[ItemID.SMALL_POTION], enemy=EnemyID.LARGE_RAT, 
            switch=(0, Direction.NORTH), desc='test', hasKey=True),
        Room(id=2, layout={
            Direction.NORTH : Door(False, -1),
            Direction.EAST : Door(False, -1),
            Direction.SOUTH : Door(False, -1),
            Direction.WEST : Door(True, 0)
        }),
        Room(id=3, layout={
            Direction.NORTH : Door(True, 0),
            Direction.EAST : Door(False, -1),
            Direction.SOUTH : Door(False, -1),
            Direction.WEST : Door(False, -1)
        }),
        Room(id=4, layout={
            Direction.NORTH : Door(False, -1),
            Direction.EAST : Door(True, 0),
            Direction.SOUTH : Door(False, -1),
            Direction.WEST : Door(False, -1)
        })
    ]),
    MapID.MAIN_MAP : Map(MapID.MAIN_MAP, intro='You find yourself in a strange, stone complex..',rooms=[
        Room(id=0, layout={
            Direction.NORTH : Door(True, 1),
            Direction.EAST : Door(),
            Direction.SOUTH : Door(),
            Direction.WEST : Door()
        }, loot=[ItemID.RUSTY_SWORD], desc='A small, dingy room, with a single door to your north. There is a Rusty Sword on the floor.'
        ),
        Room(1, layout={
            Direction.NORTH: Door(False, 8),
            Direction.EAST : Door(False, 4),
            Direction.SOUTH: Door(True, 0),
            Direction.WEST: Door(True, 2)
        }, desc='A large room with doors on all sides. A Large Rat stares at you from the corner.',
            enemy=EnemyID.LARGE_RAT
        ),
        Room(2, layout={
            Direction.NORTH: Door(False, 7),
            Direction.EAST: Door(True, 1),
            Direction.SOUTH: Door(True, 3),
            Direction.WEST: Door()
        }, loot=[ItemID.SMALL_POTION], desc='A \'T\' shaped room. There is a small potion on a table and a small switch on the wall',
            switch=(1, Direction.EAST)),
        Room(3, layout={
            Direction.NORTH: Door(True, 2),
            Direction.EAST: Door(),
            Direction.SOUTH: Door(),
            Direction.WEST: Door()
        }, desc='A dead end. There is a comically large switch on the wall.',
            switch=(2, Direction.NORTH)
        ),
        Room(4, layout={
            Direction.NORTH: Door(False, 6),
            Direction.EAST: Door(),
            Direction.SOUTH: Door(True, 5),
            Direction.WEST: Door(True, 1)
        }, enemy=EnemyID.ZOMBIE_RAT, desc='A \'T\' shaped room. A Zombie Rat shambles back and forth, paying you no mind. It reaks of decay..'
        ),
        Room(5, layout={
            Direction.NORTH: Door(True, 4),
            Direction.EAST: Door(),
            Direction.SOUTH: Door(),
            Direction.WEST: Door()
        }, loot=[ItemID.LEATHER_ARMOR], switch=(4, Direction.NORTH),
            desc='Another stone cube of a room with a grand switch on a pedistal. You\'d think the architects would pick a different shape every once and a while..\nOh! There\'s some leather armor on a mannequin',
        ),
        Room(6, layout={
            Direction.NORTH: Door(),
            Direction.EAST: Door(),
            Direction.SOUTH: Door(True, 4),
            Direction.WEST: Door()
        }, desc='An ornate study with walls of asorted books, there is a light switch on the wall. A Wizard Rat stares at you, stroking his long matted beard. There is a key around his neck.',
            enemy=EnemyID.WIZARD_RAT, hasKey=True, switch=(1, Direction.NORTH)
        ),
        Room(7, layout={
            Direction.NORTH: Door(),
            Direction.EAST: Door(),
            Direction.SOUTH: Door(True, 2),
            Direction.EAST: Door()
        }, desc='A dead end room with an ornate Chalice setting on the floor in the middle of the room.',
        loot=[ItemID.CHALICE]
        ),
        Room(8, layout={
            Direction.NORTH: Door(True),
            Direction.EAST: Door(),
            Direction.SOUTH: Door(True, 1),
            Direction.WEST: Door()
        }, enemy=EnemyID.RAT_KING, desc='The Rat King sits atop his throne of cheese, grinning at you. Yet he remains silent like all the rest.',
        isExit=True
        )
    ])
}

async def getMap(mapID: int) -> Map:
    m: Map = GAME_MAPS.get(MapID(mapID))
    return await m.newMap()

def dummy() -> Map:
    return GAME_MAPS[MapID.TEST_MAP_EMPTY]
  


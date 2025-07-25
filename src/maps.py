from enum import IntEnum
from aventure_map import *
from ascii_bulder import buildRoom
from enemies import EnemyID
from items import ItemID

class MapID(IntEnum):
    TEST_MAP_EMPTY = 0
    TEST_MAP_FIGHT = 1

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
        }, loot=[ItemID.SMALL_POTION], enemies=[EnemyID.LARGE_RAT], switch=(0, Direction.NORTH)),
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
    ])
}

def getMap(mapID: int) -> Map:
    m: Map = GAME_MAPS.get(MapID(mapID))
    return m.newMap()

def debug():
    map: Map = getMap(1)
    s = buildRoom(map.rooms[1], True, Direction.WEST)
    #print(map.rooms[0].layout[0])
    print(s)

debug()
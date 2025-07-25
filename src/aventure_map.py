from enum import IntEnum
from dataclasses import field
import copy



class Direction(IntEnum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

class Door():
    
    # Takes a door status, and adjacent room.
    # no door = open: false, adjacent = -1
    # locked door = open: false, adjacent > -1
    def __init__(self, open: bool = False, next: int = -1):
        self.open: bool = open
        self.next: int = next
    
    #attempts to unlock the 'door'
    # if its not a wall, it succeeds and returns true
    # if it is a wall, it returns false
    def unlock(self) -> bool:
        if self.next > -1:
            self.open = True
            return True
        return False
    
    def __str__(self):
        return f'open: {self.open}, next: {self.next}'


class Room():
       '''Room'''
       NO_SWITCH: tuple[int, Direction] =  (-1, Direction.NORTH)
       
       def __init__(self, id: int = 0,
                    layout: dict[Direction : Door, 
                Direction : Door, Direction : Door, Direction : Door] = {},
                    loot: list[int] = [],
                    desc: str = '',
                    ascii: str = '',
                    enemies: list[int] = [],
                    isExit: bool = False,
                    switch: tuple[int, Direction] = NO_SWITCH
                ):
           #room id
           self.id: int = id
           #layout of walls/doors
           self.layout: dict[Direction : Door, 
                Direction : Door, Direction : Door, Direction : Door] = layout
           #list of loot to find, stored as item IDs
           self.loot: list[int] = loot
           #whether room has loot
           self.hasLoot: bool = True if loot else False
           #room text description
           self.desc: str = desc
           #room ascii art depeiction
           self.ascii: str = ascii
           #list of enemies to fight, stored as enemy IDs
           self.enemies: list[int] = enemies
           # whether room has enemies.
           # used to check for combat and mark rooms as safe
           # default is decided based on enemies list
           # empty lists evaluate to fasle as boolean
           self.hasEnemies: bool = True if enemies else False
           #is this the exit room of the map
           self.isExit: bool = isExit
           #does this room have a switch
           #default is a defined NO_SWITCH
           #if tuple
           self.hasSwitch: bool = False if switch == Room.NO_SWITCH else True
           #is set True after a room switch has been flipped by player
           #only used if hasSwitch is True
           self.switchToggled: bool = False
           #room id and direction of the door the switch opens
           self.switch: tuple[int, Direction]



           

class Map():
    """
    Map repersentation for the game.
    Basically a map is an ID and a list of Room objects
    """

    def __init__(self, id: int = 0, rooms: list[Room] = []):
        self.id: int = id
        #list of rooms. keep sequential. first in list is start
        self.rooms: list[Room] = rooms
    
    # return type is in quotes to get around classes not being defined
    #until class finishes delcaration. python quirk..
    def newMap(self) -> 'Map':
        '''Returns a deepcopy of self. 
        useful for editable copies of static constants'''     
        return copy.deepcopy(self)
    
def debug():
    m = Map(0, rooms=[
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
            Direction.EAST : Door(True, 0),
            Direction.SOUTH : Door(False, -1),
            Direction.WEST : Door(False, -1)
        }),
        Room(id=3, layout={
            Direction.NORTH : Door(True, 0),
            Direction.EAST : Door(False, -1),
            Direction.SOUTH : Door(False, -1),
            Direction.WEST : Door(False, -1)
        }),
        Room(id=4, layout={
            Direction.NORTH : Door(False, -1),
            Direction.EAST : Door(False, -1),
            Direction.SOUTH : Door(False, -1),
            Direction.WEST : Door(True, 0)
        })
    ])

    print(m.rooms[0])
    
#debug()
        


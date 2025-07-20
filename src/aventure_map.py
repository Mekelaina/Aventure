from enum import IntEnum
from dataclasses import field
import copy

class Direction(IntEnum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

class Door():
    
    # Takes a direction, door status, and adjacent room.
    # no door = open: false, adjacent = -1
    # locked door = open: false, adjacent > -1
    def __init__(self, dir: Direction, open: bool = False, next: int = -1):
        self.dir: Direction = dir
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
    

class Room():
       def __init__(self, id: int = 0,
                    layout: dict[Direction : Door, 
                Direction : Door, Direction : Door, Direction : Door] = {},
                    loot: list[int] = [],
                    desc: str = '',
                    ascii: str = '',
                    enemies: list[int] = [],
                    isExit: bool = False
                ):
           #room id
           self.id: int = id
           #layout of walls/doors
           self.layout: dict[Direction : Door, 
                Direction : Door, Direction : Door, Direction : Door] = layout
           #list of loot to find, stored as item IDs
           self.loot: list[int] = loot
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



           

class Map():
    """
    Map repersentation for the game.
    Basically a map is an ID and a list of Room objects
    """

    def __init__(self, id: int = 0, rooms: list[Room] = []):
        self.id: int = id
        #list of rooms. keep sequential. first in list is start
        self.rooms: list[Room]
    
    # return type is in quotes to get around classes not being defined
    #until class finishes delcaration. python quirk..
    def newMap(self) -> 'Map':
        '''Returns a deepcopy of self. 
        useful for editable copies of static constants'''     
        return copy.deepcopy(self) 
    
    
    
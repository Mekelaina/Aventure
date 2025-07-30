from enum import IntEnum
from dataclasses import field
import copy
from items import ItemID
import asyncio




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
    async def unlock(self) -> bool:
        if self.next > -1:
            self.open = True
            return True
        return False
    
    def __str__(self):
        return f'open: {self.open}, next: {self.next}'

type Layout = dict[Direction : Door, Direction : Door, Direction : Door, Direction : Door]
type Switch = tuple[int, Direction]

class Room():
        '''Room'''
        NO_SWITCH: Switch =  (-1, Direction.NORTH)

        def __init__(self, id: int = 0,
                     layout: Layout = {},
                     loot: list[int] = [],
                     desc: str = '',
                     enemy: int = 0,
                     isExit: bool = False,
                     hasKey: bool = False,
                     switch: Switch = NO_SWITCH
                 ):
            #room id
            self.id: int = id
            #layout of walls/doors
            self.layout: Layout = layout
            #list of loot to find, stored as item IDs
            self.loot: list[int] = loot
            #whether room has loot
            self.hasLoot: bool = True if loot else False
            #room text description
            self.desc: str = desc
            #list of enemies to fight, stored as enemy IDs
            self.enemy: int = enemy
            # whether room has enemies.
            # used to check for combat and mark rooms as safe
            # default is decided based on enemy
            self.hasEnemy: bool = True if enemy > 0 else False
            #is this the exit room of the map
            self.isExit: bool = isExit
            #does this room have a switch
            #default is a defined NO_SWITCH
            #if tuple
            self.hasSwitch: bool = False if switch == Room.NO_SWITCH else True
            #is set True after a room switch has been flipped by player
            #only used if hasSwitch is True
            self.switchToggled: bool = False

            #does this room have the dungeon key needed to escape
            self.hasKey = hasKey
            #room id and direction of the door the switch opens
            self.switch: Switch = switch

        async def removeItem(self):
            self.hasLoot = False

        async def removeKey(self):
            self.hasKey = False

        async def getDoor(self, dir: Direction) -> Door:
            return self.layout[dir]
        
        async def flipSwitch(self):
            self.switchToggled = True

        async def serialize(self) :
            buff = bytearray()
            buff += self.id.to_bytes()
            buff += self.isExit.to_bytes()
            buff += self.hasSwitch.to_bytes()
            buff += self.switchToggled.to_bytes()
            buff += self.hasLoot.to_bytes()
            buff += self.hasEnemy.to_bytes()
            buff += self.hasKey.to_bytes()
            buff += self.enemy.to_bytes() #8
            
            for door in self.layout.values(): #4
                door: Door
                buff += door.open.to_bytes()
                buff += door.next.to_bytes(signed=True)
            
            buff += self.switch[0].to_bytes(signed=True)
            buff += self.switch[1].to_bytes() #2
            
            buff += len(self.loot).to_bytes()
            for l in self.loot:
                buff += l.to_bytes()
            
            buff += len(self.desc).to_bytes(length=2)
            if self.desc:
                for c in self.desc:
                    buff += c.encode()
            
            return bytes(buff)
        
        @staticmethod
        def __signed( b: int) -> int:
            return b - 256 if b >= 128 else b
        
        def deserialize(self, data: bytes) -> bool:
            if len(data) < 20:
                return False
            
            self.id = data[0]
            self.isExit = bool(data[1])
            self.hasSwitch = bool(data[2])
            self.switchToggled = bool (data[3])
            self.hasLoot = bool(data[4])
            self.hasEnemy = bool(data[5])
            self.hasKey = bool(data[6])
            self.enemy = data[7]

            self.layout = {Direction.NORTH : Door(bool(data[8]), Room.__signed(data[9])),
                           Direction.EAST : Door(bool(data[10]), Room.__signed(data[11])),
                           Direction.SOUTH : Door(bool(data[12]), Room.__signed(data[13])),
                           Direction.WEST : Door(bool(data[14]), Room.__signed(data[15]))}
            
            self.switch = (Room.__signed(data[16]), data[17])

            items = data[18]
            item_ids: list[int] = []
            if items > 0:
                for i in range(items):
                    item_ids.append(ItemID(data[19 + i]))
            self.loot = item_ids
            newi = 19 + items
            desc_len = int.from_bytes(data[newi:newi+1])
            self.desc = data[newi+2:].decode()
            
            return True
        
        def __str__(self):
            return (f'<id: {self.id}, ' 
                    f'isExit: {self.isExit}, '
                    f'hasSwitch: {self.hasSwitch}, '
                    f'switchToggled: {self.switchToggled}, '
                    f'hasLoot: {self.hasLoot}, '
                    f'hasEnemy: {self.hasEnemy}, '
                    f'enemy: {self.enemy}, '
                    f'layout: [N: {self.layout[Direction.NORTH]}], '
                    f'layout: [E: {self.layout[Direction.EAST]}], '
                    f'layout: [S: {self.layout[Direction.SOUTH]}], '
                    f'layout: [W: {self.layout[Direction.WEST]}], '
                    f'switch: [{self.switch[0]}, {self.switch[1]}], '
                    f'loot: {self.loot}, '
                    f'desc: {self.desc}>')
            


            
            
            
async def _chop( data: bytearray) -> list[bytearray]:
    # buff = bytearray()
    # for idx, b in enumerate(data):
    count = 0
    #print(count)
    #print(data)
    for i in range(len(data)):
        #print('dfsa')
        await asyncio.sleep(0)
        if data[i] == 254:
            count += 1
        else:
            count = 0
        
        if count == 2:
            return (data[0:i-1], data[i+1:])


class Map():
    """
    Map repersentation for the game.
    Basically a map is an ID and a list of Room objects
    """

    def __init__(self, id: int = 0, rooms: list[Room] = [], intro=''):
        self.id: int = id
        #list of rooms. keep sequential. first in list is start
        self.rooms: list[Room] = rooms
        self.intro = intro
    
    # return type is in quotes to get around classes not being defined
    #until class finishes delcaration. python quirk..
    async def newMap(self) -> 'Map':
        '''Returns a deepcopy of self. 
        useful for editable copies of static constants'''     
        return copy.deepcopy(self)
    
    async def serialize(self) -> tuple[int, bytes]:
        buff = bytearray()
        
        for room in self.rooms:
            buff += await room.serialize()
            buff.append(254)
            buff.append(254)
        return (self.id, bytes(buff))
          
    async def deserialize(self, data: tuple[int, bytes]) -> bool:
        buff = []
        loop = True
        
        self.id = data[0]
        mut_data = bytearray(data[1])
        while loop:
            x, y = await _chop(mut_data)
            await asyncio.sleep(0)
            buff.append(x)
            mut_data = y
            if not mut_data:
                loop = False
       
        r: list[Room] = []
        for b in buff:
            room = Room()
            room.deserialize(b)
            r.append(room)
        self.rooms = r
            
        return True

    def __str__(self):
        buff = '{{'
        for x, room in enumerate(self.rooms):
            buff += str(room)
            if x < len(self.rooms)-1:
                buff += ', '
        buff += '}}'
        return buff
            
    
    

    async def getRoom(self, roomID: int) -> Room:
        return self.rooms[roomID]
    
    async def setRoom(self, roomID: int, room: Room):
        self.rooms[roomID] = room

    async def isValidRoom(self, roomID) -> bool:
        if roomID >= 0 and roomID < len(self.rooms):
            #print(True)
            return True
        else:
            #print(False)
            return False
        


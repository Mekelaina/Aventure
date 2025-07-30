from dataclasses import dataclass
from enum import IntEnum
from items import *
from aventure_equipslot import EquipSlot
from aventure_map import Direction


# current state of player
class GameState(IntEnum):
    NORUN_MENU = 0
    RUN_DUNGEON = 1
    RUN_COMBAT = 2
    RUN_MENU = 3
    FINISH_MARKET = 4

type statsData = tuple[int, int, int, int, int, int, int]
type playerData = tuple[int, int, int, int, int, int, int, int, int, int, int, int]
type equipmentData = tuple[int, int, int, int, int, int, int, int]
type choiceData = tuple[int, int]
# player stats in dataclass to make writing to DB cleaner
@dataclass
class GlobalStats:
    dungeonsCleared: int = 0
    enemiesKilled: int = 0
    deaths: int = 0
    totalGold: int = 0
    totalItems: int = 0
    messagesSent: int = 0

    async def serialize(self) -> statsData:
        return (self.dungeonsCleared, 
                self.enemiesKilled, 
                self.deaths, 
                self.totalGold, 
                self.totalItems, 
                self.messagesSent)
    
    async def deserialize(self, data: statsData) -> None:
        (self.dungeonsCleared, 
        self.enemiesKilled, 
        self.deaths, 
        self.totalGold, 
        self.totalItems, 
        self.messagesSent) = data


# player data in a dataclass to make writing to DB easier
@dataclass
class Data:
    level: int  = 1
    maxHealth: int  = 10
    currHealth: int = 10
    baseAttack: int = 1
    baseDefence: int = 1
    exp: int = 0
    gold: int = 0
    isAlive: bool = True
    map: int = -1
    room: int = -1
    lastMove: Direction = Direction.NORTH
    hasMoved: bool = False

#order of values is the order their stored in db
    async def serialize(self) -> playerData:
        return (self.level, 
                self.maxHealth, 
                self.currHealth,
                self.baseAttack,
                self.baseDefence,
                self.exp,
                self.gold,
                int(self.isAlive),
                self.map,
                self.room,
                self.lastMove.value,
                int(self.hasMoved))
    
    async def deserialize(self, data: playerData):
        #print(f'data coming in: {data}')
        self.level = data[0]
        self.maxHealth = data[1] 
        self.currHealth = data[2]
        self.baseAttack = data[3]
        self.baseDefence = data[4]
        self.exp = data[5]
        self.gold = data[6]
        self.isAlive = bool(data[7])
        self.map = data[8]
        self.room = data[9]
        self.lastMove = Direction(data[10])
        self.hasMoved = bool(data[11])

        #print(f'after assing: {self.map}, {self.room}')


@dataclass
class InvItem():
    itemID: int
    #count is only used in inventory and consumables
    count: int

    def to_bytes(self) -> bytes:
        return bytes([self.itemID, self.count])
        



@dataclass
class Equipment():
    key: bool
    weapon: InvItem
    armor: InvItem
    offhand: InvItem
    consumeable1: InvItem
    consumeable2: InvItem

    async def equipItem(self, item: InvItem, slot: EquipSlot):
        match slot:
            case EquipSlot.WEAPON:
                self.weapon = item
            case EquipSlot.ARMOR:
                self.armor = item
            case EquipSlot.OFFHAND:
                self.offhand = item
            case EquipSlot.CONSUMEABLE_1:
                self.consumeable1 = item
            case EquipSlot.CONSUMEABLE_2:
                self.consumeable2 = item
            
    
    async def isEquiped(self, slot: EquipSlot) -> bool:
        match slot:
            case EquipSlot.WEAPON:
                if self.weapon == Player.EMPTY_INV:
                    return False
                return True
            case EquipSlot.ARMOR:
                if self.armor == Player.EMPTY_INV:
                    return False
                return True
            case EquipSlot.OFFHAND:
                if self.offhand == Player.EMPTY_INV:
                    return False
                return True
            case EquipSlot.CONSUMEABLE_1:
                if self.consumeable1 == Player.EMPTY_INV:
                    return False
                return True
            case EquipSlot.CONSUMEABLE_2:
                if self.consumeable2 == Player.EMPTY_INV:
                    return False
                return True
    
    #return form for writing to DB
    async def serialize(self) -> equipmentData:
        return (int(self.key),
                self.weapon.itemID, 
                self.armor.itemID, 
                self.offhand.itemID,
                self.consumeable1.itemID,
                self.consumeable1.count,
                self.consumeable2.itemID,
                self.consumeable2.count)
    
    #parse data from db back into object
    async def deserialize(self, data: equipmentData):
        #this is messy, but its just tuple unpacking
        self.key,
        self.weapon.itemID, 
        self.armor.itemID, 
        self.offhand.itemID, 
        self.consumeable1.itemID,
        self.consumeable1.count,
        self.consumeable2.itemID,
        self.consumeable2.count = data
        #type casting to insure key is bool
        self.key = bool(self.key)
        #the counts arent used for weapon, armor, offhand
        self.weapon.count = 0
        self.armor.count = 0
        self.offhand.count = 0



class PlayerInventory:

    def __init__(self):
        #number of different items in list, aka list size
        self.currSize: int = 0
        self.items: list[InvItem] = []

    def __str__(self):
        return f'Inv:  {{{self.currSize}, {self.items}}}'
    
    #return form of data for writing to db
    async def serialize(self) -> bytes:
        res = bytearray()
        res.extend(self.currSize.to_bytes(length=2))
        for i in range(self.currSize):
            res.append(self.items[i].itemID)
            res.append(self.items[i].count)
        return bytes(res)
    
    #read data from db and parse it into object variables
    async def deserialize(self, blob: bytes) -> bool:
        if len(blob) < 2:
            return False
        
        buff: list[InvItem] = []
        self.currSize = int.from_bytes(blob[0:2])
        if self.currSize > 0:
            con = blob[2:]
            for i in range(0, len(con), 2):
                buff.append(InvItem(ItemID(con[i]), con[i+1]))
            self.items.clear()
            self.items.extend(buff)
            return True

    #checks if a given itemID is in the inventory
    # returns index if it exists
    # else -1
    async def hasItem(self, item: InvItem) -> int:
        for i in range(self.currSize):
            if self.items[i].itemID == item.itemID:
                return i
        return -1
    
    async def itemCount(self, item: InvItem) -> int:
        for i in range(self.currSize):
            if self.items[i].itemID == item.itemID:
                return self.items[i].count
        return 0

    async def addItem(self, item: InvItem):
        print(f'adding Item {item}')
        i = await self.hasItem(item)
        if i == -1:
            self.items.append(item)
            self.currSize += 1
        else:
            self.items[i].count += item.count

    # attempts to consume (decrement) an item from the inventory
    # despite taking an InvItem, count doesnt matter
    # returns:
    # -1 if itemID is not in inventory
    # 0 if item is consumed, but others of its type exist
    # 1 if item is used up completely
    def consumeItem(self, item: InvItem) -> int:
        i = self.hasItem(item)
        if i == -1:
            return -1
        if (self.items[i].count - 1) > 0:
            self.items[i].count -= 1
            return 0
        elif (self.items[i].count - 1) == 0:
            self.items.pop(i)
            self.currSize -= 1
            return 1
        else:
            #this *should* never happen, if it does, somethings broken
            return -2

    async def removeItem(self, item: InvItem) -> bool:
        i = await self.hasItem(item)
        if i >= 0:
            self.items.pop(i)
            self.currSize -= 1
    
    async def clearInv(self):
        self.items.clear()
        self.currSize = 0


@dataclass
class Choice:
    doDelete: bool = 0
    doNew: bool = 0

    async def serialize(self) -> tuple[int, int]:
        return (int(self.doDelete), int(self.doNew))
    
    async def deserialize(self, data: tuple[int, int]) -> None:
        self.doDelete, self.doNew = data
        self.doDelete = bool(self.doDelete)
        self.doNew = bool(self.doNew)

class Player:
    #empty inventory slot is a "null item"
    #this is fine as a static value
    #since itll be the same for all player objects
    #although there shouldnt be more than one player at a time..
    #as far as code goes
    EMPTY_INV: InvItem = InvItem(0, 0)

    # hardcoded list of valid mappings between item equipable property
    # and equipment slots, since the magic numbers dont line up
    # simplifies matching code
    VALID_EQUIPS: list[tuple[int, int]] = [
        (Equipable.WEAPON, EquipSlot.WEAPON), 
        (Equipable.ARMOR, EquipSlot.ARMOR),
        (Equipable.OFFHAND, EquipSlot.OFFHAND),
        (Equipable.CONSUMABLE, EquipSlot.CONSUMEABLE_1),
        (Equipable.CONSUMABLE, EquipSlot.CONSUMEABLE_2)
        ]

    def __init__(self):
        self.data: Data = Data()
        self.stats: GlobalStats = GlobalStats()
        self.state: GameState = GameState.NORUN_MENU
        #two inventories. one to hold items aquired on current run
        #to lose in case of death
        #colated upon death or victory
        self.runInv: PlayerInventory = PlayerInventory()
        self.postInv: PlayerInventory = PlayerInventory()
        self.equipment: Equipment = Equipment(False,
            self.EMPTY_INV, self.EMPTY_INV, self.EMPTY_INV, self.EMPTY_INV, self.EMPTY_INV)
        self.choice = Choice()
    
    async def setRoom(self, romId: int):
        self.data.room = romId
    
    async def getHasMoved(self) -> bool:
        return self.data.hasMoved
    
    async def getLastMove(self) -> Direction:
        return self.data.lastMove
    
    async def setHasMoved(self, value: bool):
        self.data.hasMoved = value
    
    async def setLastMove(self, value: Direction):
        self.data.lastMove = value

    def takeDamage(self, dmg: int) -> None:
        res = dmg - self.getDeffence()
        
        if (self.data.currHealth - res) <= 0:
            self.data.currHealth = 0
            self.data.isAlive = 0
            # todo change state
        else:
            self.data.currHealth -= res
    
    def healSelf(self, amt: int) -> None:
        if (self.data.currHealth + amt) >= self.data.maxHealth:
            self.data.currHealth = self.data.maxHealth
    
    async def equipItem(self, itemID: int, count: int, slot: EquipSlot) -> bool:
        itemData: AventureItem = await getItemEquipable(itemID)
        canEquip = await self.canEquipItem(itemData, slot)
        if canEquip:
            await self.equipment.equipItem(InvItem(itemID, count), slot)
            return True
        return False
    
    async def unequipItem(self, slot: EquipSlot) -> None:
        await self.equipment.equipItem(self.EMPTY_INV, slot)
         
    async def canEquipItem(self, itemEquipVal: Equipable, itemSlot: EquipSlot) -> bool:
        self.VALID_EQUIPS
        match (itemEquipVal.value, itemSlot.value):
            case (x, y) if (x, y) in self.VALID_EQUIPS:
                return True
            case _:
                return False
    
    #returns true upon a levelup
    def addExp(self, amt: int) -> bool:
        self.data.exp += amt
        return False
        # TODO: add level up mechanics
    
    def addGold(self, amt: int):
        self.data.gold += amt
        self.stats.totalGold += amt

    # checks if player has enough gold to "spend" for amt
    # returns true if yes, updates gold
    # false if no, amount stays the same
    def spendGold(self, amt: int) -> bool:
        if (self.data.gold - amt) < 0:
            return False
        else:
            self.data.gold -= amt
            return True
    
    async def getAttack(self) -> int:
        if self.equipment.isEquiped(EquipSlot.WEAPON):
            return self.data.baseAttack + getItemMod(self.equipment.weapon.itemID)
        else:
            return self.data.baseAttack
    
    async def getDeffence(self) -> int:
        if self.equipment.isEquiped(EquipSlot.ARMOR):
            return self.data.baseDefence + await getItemMod(self.equipment.armor.itemID)
        else:
            return self.data.baseDefence
        
    async def hasKey(self) -> bool:
        return self.equipment.key
    
    async def giveKey(self):
        self.equipment.key = True
    
    async def takeKey(self):
        self.equipment.key = False
    
    async def restart(self, map: int):
        self.state = GameState.RUN_DUNGEON
        self.data.map = map
        self.data.room = 0
        self.data.hasMoved = False
        self.data.isAlive = True
        self.data.currHealth = self.data.maxHealth
        
        await self.runInv.clearInv()
        await self.runInv.addItem(InvItem(ItemID.CLOTHES, 1))
        await self.runInv.addItem(InvItem(ItemID.POCKET_KNIFE, 1))
        await self.takeKey()
    
    async def getInv(self):
        return self.runInv
    
    async def getEquipment(self):
        return self.equipment
    
    async def giveItem(self, id: int, count: int):
        await self.runInv.addItem(InvItem(id, count))
    
    async def save(self) -> list[int, playerData, equipmentData, 
                          statsData, bytes, bytes, choiceData]:
        player_data = []
        player_data.append(self.state)
        
        player_data.append(await self.data.serialize())
        
        player_data.append(await self.stats.serialize())
        
        player_data.append(await self.equipment.serialize())
       
        player_data.append(await self.runInv.serialize())
       
        player_data.append(await self.postInv.serialize())

        player_data.append(await self.choice.serialize())
        
        return player_data
    
    async def load(self, data: list[int, playerData, statsData, 
                          equipmentData, bytes, bytes, choiceData]):
        self.state = data.pop(0)
        await self.data.deserialize(data.pop(0))
        await self.stats.deserialize(data.pop(0))
        await self.equipment.deserialize(data.pop(0))
        await self.runInv.deserialize(data.pop(0))
        await self.postInv.deserialize(data.pop(0))


        

  




    

#debug()
    

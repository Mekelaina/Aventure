from dataclasses import dataclass
from enum import IntEnum
from items import *
from aventure_map import Direction


# current state of player
class GameState(IntEnum):
    NORUN_MENU = 0
    RUN_DUNGEON = 1
    RUN_COMBAT = 2
    RUN_MENU = 3
    FINISH_MARKET = 4

# player stats in dataclass to make writing to DB cleaner
@dataclass
class GlobalStats:
    dungeonsCleared: int = 0
    enemiesKilled: int = 0
    deaths: int = 0
    totalGold: int = 0
    totalItems: int = 0
    messagesSent: int = 0


# player data in a dataclass to make writing to DB easier
@dataclass
class Data:
    level: int  = 1
    maxHealth: int  = 10
    currHealth: int = 10
    isAlive: bool = 1
    baseAttack: int = 1
    baseDefence: int = 1
    exp: int = 0
    gold: int = 0
    lastMove: Direction = Direction.NORTH
    hasMoved: bool = False
    map: int = -1
    room: int = -1


@dataclass
class InvItem():
    itemID: int
    #count is only used in inventory and consumables
    count: int

    def to_bytes(self) -> bytes:
        return bytes([self.itemID, self.count])
        
class EquipSlot(IntEnum):
    WEAPON = 0
    ARMOR = 1
    OFFHAND = 2
    CONSUMEABLE_1 = 3
    CONSUMEABLE_2 = 4

@dataclass
class Equipment():
    key: bool
    weapon: InvItem
    armor: InvItem
    offhand: InvItem
    consumeable1: InvItem
    consumeable2: InvItem

    def equipItem(self, item: InvItem, slot: EquipSlot):
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
            
    
    def isEquiped(self, slot: EquipSlot) -> bool:
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
    def serialize(self) -> tuple[int, int, int, int, int, int, int, int]:
        return (int(self.key),
                self.weapon.itemID, 
                self.armor.itemID, 
                self.offhand.itemID,
                self.consumeable1.itemID,
                self.consumeable1.count,
                self.consumeable2.itemID,
                self.consumeable2.count)
    
    #parse data from db back into object
    def deserialize(self, data: tuple[int, int, int, int, int, int, int, int]):
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
    def serialize(self) -> bytes:
        res = bytearray()
        res.extend(self.currSize.to_bytes(length=2))
        for i in range(self.currSize):
            res.append(self.items[i].itemID)
            res.append(self.items[i].count)
        return bytes(res)
    
    #read data from db and parse it into object variables
    def deserialize(self, blob: bytes) -> bool:
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
    def hasItem(self, item: InvItem) -> int:
        for i in range(self.currSize):
            if self.items[i].itemID == item.itemID:
                return i
        return -1

    def addItem(self, item: InvItem):
        i = self.hasItem(item)
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

    def removeItem(self, item: InvItem) -> bool:
        i = self.hasItem(item)
        if i >= 0:
            self.items.pop(i)
            self.currSize -= 1


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
        self.equipment: Equipment = Equipment(
            self.EMPTY_INV, self.EMPTY_INV, self.EMPTY_INV, self.EMPTY_INV, self.EMPTY_INV)
    
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
    
    def equipItem(self, itemID: int, count: int, slot: EquipSlot) -> bool:
        itemData: AventureItem = getEquipable(itemID)
        if self.canEquipItem(itemData, slot):
            self.equipment.equipItem(InvItem(itemID, count), slot)
            return True
        return False
    
    def unequipItem(self, slot: EquipSlot) -> None:
        self.equipment.equipItem(self.EMPTY_INV, slot)
         
    def canEquipItem(self, itemEquipVal: Equipable, itemSlot: EquipSlot) -> bool:
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
    
    def getAttack(self) -> int:
        if self.equipment.isEquiped(EquipSlot.WEAPON):
            return self.data.baseAttack + getMod(self.equipment.weapon.itemID)
        else:
            return self.data.baseAttack
    
    def getDeffence(self) -> int:
        if self.equipment.isEquiped(EquipSlot.ARMOR):
            return self.data.baseDefence + getMod(self.equipment.armor.itemID)
        else:
            return self.data.baseDefence
        
    def hasKey(self) -> bool:
        return self.equipment.key
    
    def giveKey(self):
        self.equipment.key = True
    
    def takeKey(self):
        self.equipment.key = False
    
    def restart(self, map: int):
        self.state = GameState.RUN_DUNGEON
        self.data.map = map
        self.data.room = 0
        self.data.hasMoved = False
        self.data.isAlive = True
        self.data.currHealth = self.data.maxHealth
        self.takeKey()
            
def debug():
   p = PlayerInventory()
   q = PlayerInventory()
   p.addItem(InvItem(ItemID.RUSTY_SWORD, 1))
   p.addItem(InvItem(ItemID.SMALL_POTION, 5))
   p.addItem(InvItem(ItemID.NULL_ITEM, 0))
   
   print(p)
   b = p.serialize()
   print(b)

   q.deserialize(b)
   print(q)

  




    

#debug()
    

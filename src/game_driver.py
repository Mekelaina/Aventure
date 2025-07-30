from aventure_player import Player, GameState, InvItem, EquipSlot
from maps import getMap, dummy, MapID
from aventure_map import Room, Map, Direction, Door
from aventure_enemy import *
from items import ItemID, Equipable, getItem, getItemDesc, getItemByName, getItemEquipable, getSlotFromItem
from aventure_item import AventureItem
from enemies import getEnemy, EnemyID
import aventure_db as db
from ascii_bulder import buildRoom
#import sqlite3


def checkForBattle(map: Map, player: Player) -> bool:
    room = map.rooms[player.data.room]
    if room.hasEnemies:
        return True
    return False


_DIR: dict[Direction, str] = {
    Direction.NORTH : 'You move north.',
    Direction.EAST : 'You move east',
    Direction.SOUTH : 'You move south',
    Direction.WEST : 'You move west'
}

class Game:
    def __init__(self):
        self.player: Player = Player()
        self.map: Map = dummy()
        self.enemy: GameEnemy = GameEnemy()

    async def newGame(self, mapID: MapID):
        await self.player.restart(mapID)
        self.map = await getMap(mapID)
    
    async def messageIncrement(self)-> None:
        self.player.stats.messagesSent += 1

    async def clearDungeonIncrement(self) -> None:
        self.player.stats.dungeonsCleared += 1
    
    async def setState(self, newState: GameState) -> None:
        self.player.state = newState

    async def setDoDelete(self, value: bool) -> None:
        self.player.choice.doDelete = value
    
    async def setDoNew(self, value: bool) -> None:
        self.player.choice.doNew = value

    async def isDoDelete(self) -> bool:
        return self.player.choice.doDelete
    
    async def isDoNew(self) -> bool:
        #print('wh')
        return self.player.choice.doNew
    
    async def getRoomAscii(self) -> str:
        room = await self.map.getRoom(self.player.data.room)
        hasMoved = await self.player.getHasMoved()
        lastMove = await self.player.getLastMove()
        res = await buildRoom(room, hasMoved, lastMove)
        return res
    
    async def getMapIntro(self) -> str:
        return self.map.intro
    
    async def getRoomDesc(self) -> str:
        r = await self.map.getRoom(self.player.data.room)
        #print(self.player.data.room)
        #print(r)
        return r.desc
    
    async def roomHasEnemy(self) -> bool:
        r = await self.map.getRoom(self.player.data.room)
        #print(r)
        if r.hasEnemy:
            return True
        else:
            return False
    
    async def getRoomEnemyDesc(self) -> str:
        r: Room = await self.map.getRoom(self.player.data.room)
        e: GameEnemy = await getEnemy(r.enemy)
        return f'{e.name} ({e.ascii}) -- {e.desc}'

    async def roomHasItem(self) -> bool:
        r = await self.map.getRoom(self.player.data.room)
        if r.hasLoot:
            return True
        else:
            return False
    
    async def roomHasSwitch(self) -> bool:
        r = await self.map.getRoom(self.player.data.room)
        if r.hasSwitch:
            return True
        else:
            return False
        
    async def roomSwitchToggled(self) -> bool:
        r = await self.map.getRoom(self.player.data.room)
        if r.switchToggled:
            return True
        else:
            return False
    
    async def roomHasKey(self) -> bool:
        r = await self.map.getRoom(self.player.data.room)
        if r.hasKey:
            return True
        else:
            return False
        
    async def roomFlipSwitch(self):
        playerRoom = await self.map.getRoom(self.player.data.room)
        switch = playerRoom.switch
        targetRoom = await self.map.getRoom(switch[0])
        targetDoor = await targetRoom.getDoor(switch[1])
        await targetDoor.unlock()
        await playerRoom.flipSwitch()
        await self.map.setRoom(playerRoom.id, playerRoom)
        await self.map.setRoom(targetRoom.id, targetRoom)
        

    async def lookItem(self, itemName: str) -> str:
        item = await getItemByName(itemName)
        if item.id == ItemID.NULL_ITEM:
            return f'There\'s no `{itemName}` here..'
        else:
            return f'{item.name}: {item.description}'
        
    async def playerHasItem(self, itemName: str) -> bool:
        item = await getItemByName(itemName)
        if item.id == ItemID.NULL_ITEM:
            return False
        else:
            i = await self.player.runInv.hasItem(InvItem(item.id, 1))
            if i != -1:
                return True
            else:
                return False
    
    #only called after playerHasItem is true
    async def playerEquipItem(self, itemName: str) -> tuple[bool, str]:
        inv = await self.player.getInv()
        item = await getItemByName(itemName)
        if item.id == ItemID.NULL_ITEM:
            return (False, f'No item `{itemName}`')
        else:
            itemCount = await inv.itemCount(InvItem(item.id, 1))
            itemEq = await getItemEquipable(item.id)
            print(itemEq)
            if itemEq == Equipable.NO_EQUIP:
                return (False, f'Cant equip item `{itemName}`')
            else:
                slot = await getSlotFromItem(item.id)
                if slot == EquipSlot.CONSUMEABLE_1:
                    filled = await self.player.equipment.isEquiped(slot)
                    if filled:
                        await self.player.equipItem(item.id, itemCount, EquipSlot.CONSUMEABLE_2)
                        return (True, f'You Equiped x{itemCount} {item.name} into Consumable B')
                    else:
                        await self.player.equipItem(item.id, itemCount, slot)
                        (True, f'You Equiped x{itemCount} {item.name} into Consumable A')
                    
                else:
                    await self.player.equipItem(item.id, itemCount, slot)
                    match slot:
                        case EquipSlot.WEAPON:
                            return (True, f'You Equiped {item.name} into Weapon')
                        case EquipSlot.ARMOR:
                            return (True, f'You Equiped {item.name} into Armor')
                        case EquipSlot.OFFHAND:
                            return (True, f'You Equiped {item.name} into Offhand')
                        
    async def playerTakeKey(self):
        print('taking key')
        r = await self.map.getRoom(self.player.data.room)
        await r.removeKey()
        await self.player.giveKey()
        await self.map.setRoom(r.id, r)

    async def playerTakeItem(self) -> str:
        room = await self.map.getRoom(self.player.data.room)
        item = await getItem(room.loot[0])
        await self.player.giveItem(item.id, 1)
        print(self.player.runInv.items)
        await room.removeItem()
        print(room)
        await self.map.setRoom(room.id, room)
        return item.name

    async def getInv(self) -> str:
        inv = await self.player.getInv()
        rtn = '---- Inventory ----\n'
        print('a')
        print(inv.items)
        for i in inv.items:
            print(i)
            item = await getItem(i.itemID)
            rtn += f'{item.name} x{i.count}'
            rtn += '\n'
        print('d')
        rtn = rtn[:-1]
        return rtn 
    
    async def getEquipment(self) -> str:
        eq = await self.player.getEquipment()
        weapon = await getItem(eq.weapon.itemID)
        armor = await getItem(eq.armor.itemID)
        offhand = await getItem(eq.offhand.itemID)
        con1 = await getItem(eq.consumeable1.itemID)
        con2 = await getItem(eq.consumeable2.itemID)

        k = 'Yes' if eq.key else 'No'
        rtn = f'''--- Equipment ---
Weapon: {weapon.name} | Armor: {armor.name} | Offhand: {offhand.name}
Consumable A: {con1.name} x{eq.consumeable1.count} | Consumable B: {con2.name} x{eq.consumeable2.count} | Key: {k}'''
        return rtn


    # -1: error
    #  0: door locked
    #  1: door unlocked, moved successfully
    #  2: wall
    #  3: exit
    async def move(self, dir: Direction) -> tuple[int, str]:
        r: Room = await self.map.getRoom(self.player.data.room)
        door: Door = r.layout[dir]
        isValid = await self.map.isValidRoom(door.next)
        print(f'{r}, {dir}')
        if door.open:
            if door.next == -1 and r.isExit:
                #exit
                return (3, 'You completed the dungeon!')
                pass
            elif isValid:
                #move
                await self.player.setRoom(door.next)
                await self.player.setHasMoved(True)
                await self.player.setLastMove(dir)
                return (1, _DIR[dir])
                pass
            else:
                #err
                return (-1, 'Error: Invalid state')
        else:
            if door.next == -1:
                #wall
                return (2, f'You attempt to run through the wall... *THUD*')
                pass
            elif isValid:
                #locked
                return (0, 'The door is locked tight. Perhaps there is a way to open it?')
                pass
            else:
                #err
                return (-1, 'Error: Invalid state')
    
    
        
        




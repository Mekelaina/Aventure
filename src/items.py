from aventure_item import AventureItem, Usecase, Equipable
from aventure_equipslot import EquipSlot
from enum import IntEnum, auto

#This file holds all the created game item objects and their ID's

class ItemID(IntEnum):
    NULL_ITEM = 0
    RUSTY_SWORD = 1
    SMALL_POTION = 2
    POCKET_KNIFE = 3
    CLOTHES = 4
    CHALICE = 5
    LEATHER_ARMOR = 6


GAME_ITEMS = {
        ItemID.NULL_ITEM: AventureItem(),
        ItemID.RUSTY_SWORD: AventureItem(ItemID.RUSTY_SWORD,'Rusty Sword', 
            'A rusty, brittle sword. +3 ATK', 1, 3, Usecase.BUFF_ATK, Equipable.WEAPON),
        ItemID.SMALL_POTION: AventureItem(ItemID.SMALL_POTION,'Small Potion',
            'A small healing potion. +5 hp', 5, 5, Usecase.HEAL_USER, Equipable.CONSUMABLE),
        ItemID.POCKET_KNIFE: AventureItem(ItemID.POCKET_KNIFE,'Pocket Knife', 'Useful, but not practical. A last-resort tool with limited reach. +2 ATK',
        5, 2, Usecase.BUFF_ATK, Equipable.WEAPON),
        ItemID.CLOTHES: AventureItem(ItemID.CLOTHES,'Clothes', 'Everyday clothing with no protective use. You\'re basically asking for trouble. +1 DEF',
        1, 1, Usecase.BUFF_DEF, Equipable.ARMOR),
        ItemID.CHALICE: AventureItem(ItemID.CHALICE,'Chalice', 'A Solid gold chalice that glitters in the torchlight', 200),
        ItemID.LEATHER_ARMOR: AventureItem(ItemID.LEATHER_ARMOR,'Leather Armor', 'A Leather tunic with undicernable stains. +3 DEF',
        20, 3, Usecase.BUFF_DEF, Equipable.ARMOR)

}

# getter functions to clean up getting item properties from table
async def getItem(id: int) -> AventureItem:
    return GAME_ITEMS[id]

async def getItemName(id: int) -> str:
    return GAME_ITEMS[id].name

async def getItemDesc(id: int) -> str:
    return GAME_ITEMS[id].description

async def getItemValue(id: int) -> int:
    return GAME_ITEMS[id].value

async def getItemMod(id: int) -> int:
    return GAME_ITEMS[id].mod

async def getItemUsecase(id: int) -> Usecase:
    return GAME_ITEMS[id].use

async def getItemEquipable(id: int) -> Equipable:
    print(GAME_ITEMS[id].equip)
    return GAME_ITEMS[id].equip

async def getItemByName(name: str) -> AventureItem:
    for item in GAME_ITEMS.values():
        if item.name.lower() == name:
            return item
    return GAME_ITEMS[0]

async def getSlotFromItem(id: int) -> EquipSlot:
    item = GAME_ITEMS[id]
    match item.equip:
        case Equipable.WEAPON:
            return EquipSlot.WEAPON
        case Equipable.ARMOR:
            return EquipSlot.ARMOR
        case Equipable.OFFHAND:
            return EquipSlot.OFFHAND
        case Equipable.CONSUMABLE:
            return EquipSlot.CONSUMEABLE_1

from aventure_item import AventureItem, Usecase, Equipable
from enum import IntEnum, auto

#This file holds all the created game item objects and their ID's

class ItemID(IntEnum):
    NULL_ITEM = 0
    RUSTY_SWORD = auto()
    SMALL_POTION = auto()




GAME_ITEMS = {
        ItemID.NULL_ITEM: AventureItem(),
        ItemID.RUSTY_SWORD: AventureItem('Rusty Sword', 
            'A rusty, brittle sword. +2 ATK', 1, 2, Usecase.BUFF_ATK, Equipable.WEAPON),
        ItemID.SMALL_POTION: AventureItem('Small Potion',
            'A small healing potion. +5 hp', 5, 5, Usecase.HEAL_USER, Equipable.CONSUMABLE)
}

# getter functions to clean up getting item properties from table
def getItem(id: int) -> AventureItem:
    return GAME_ITEMS[id]

def getName(id: int) -> str:
    return GAME_ITEMS[id].name

def getDesc(id: int) -> str:
    return GAME_ITEMS[id].description

def getValue(id: int) -> int:
    return GAME_ITEMS[id].value

def getMod(id: int) -> int:
    return GAME_ITEMS[id].mod

def getUsecase(id: int) -> Usecase:
    return GAME_ITEMS[id].use

def getEquipable(id: int) -> Equipable:
    return GAME_ITEMS[id].equip


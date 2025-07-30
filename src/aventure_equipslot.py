from enum import IntEnum

#this class is just a bodge to solve an import conflict 

class EquipSlot(IntEnum):
    WEAPON = 0
    ARMOR = 1
    OFFHAND = 2
    CONSUMEABLE_1 = 3
    CONSUMEABLE_2 = 4
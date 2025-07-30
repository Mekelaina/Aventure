from dataclasses import dataclass, field
from itertools import count
from enum import IntEnum


# Item Definitions
class Usecase(IntEnum):
    '''Usecase Enum an Item can have.\n
    NO_USE: 0, BUFF_ATK: 1, BUFF_DEF: 2, HEAL_USER: 3, HURT_ENEMY: 4'''
    NO_USE     = 0
    BUFF_ATK   = 1
    BUFF_DEF   = 2
    HEAL_USER  = 3
    HURT_ENEMY = 4

class Equipable(IntEnum):
    '''What equipment slot an Item can be equiped in\n
    NO_EQUIP: 0, WEAPON: 1, ARMOR: 2, OFFHAND: 3, CONSUMABLE: 4'''
    NO_EQUIP   = 0
    WEAPON     = 1
    ARMOR      = 2
    OFFHAND    = 3
    CONSUMABLE = 4

@dataclass
class AventureItem:

    # this mess is just to autoincrement ID each time the constructor is called
    # id: int = field(default_factory=lambda counter=count(): next(counter))
    id: int = 0
    name: str = 'empty'
    description: str = ''
    value: int = 0
    mod: int = 0
    use: Usecase = Usecase.NO_USE
    equip: Equipable = Equipable.NO_EQUIP


def debug():
  pass

debug()


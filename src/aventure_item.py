from dataclasses import dataclass, field
from itertools import count
from enum import Enum

class Usecase(Enum):
    NO_USE     = 0
    BUFF_ATK   = 1
    BUFF_DEF   = 2
    HEAL_USER  = 3
    HURT_ENEMY = 4

class Equipable(Enum):
    NO_EQUIP   = 0
    WEAPON     = 1
    ARMOR      = 2
    OFFHAND    = 3
    CONSUMABLE = 4

@dataclass
class Item:

    # this mess is just to autoincrement ID each time the constructor is called
    id: int = field(default_factory=lambda counter=count(): next(counter))
    name: str = 'NULL'
    description: str = 'NULL'
    value: int = 0
    mod: int = 0
    use: Usecase = Usecase.NO_USE
    equip: Equipable = Equipable.NO_EQUIP

def debug():
    i1 = Item()
    i2 = Item(name='foo', description='bar')

    print(i1)
    print(i2)

debug()


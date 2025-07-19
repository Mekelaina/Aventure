from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple
from aventure_item import *

class State(Enum):
    NORUN_MENU = 0
    RUN_DUNGEON = 1
    RUN_COMBAT = 2
    RUN_MENU = 3
    FINISH_MARKET = 4

@dataclass
class GlobalStats:
    dungeonsCleared: int = 0
    enemiesKilled: int = 0
    deaths: int = 0
    totalGold: int = 0
    totalItems: int = 0

@dataclass
class Data:
    level: int  = 0
    maxHealth: int  = 0
    currhealth: int = 0
    attack: int = 0
    defence: int = 0
    exp: int = 0
    gold: int = 0

class InvItem(NamedTuple):
    itemID: int
    count: int

class Player:

    def __init__(self):
        self.data: Data = Data()
        self.stats: GlobalStats = GlobalStats()
        self.state: State = State.NORUN_MENU
        self.inv: list[InvItem] = []
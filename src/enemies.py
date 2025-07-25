from enum import IntEnum
from aventure_enemy import *

class EnemyID(IntEnum):
    LARGE_RAT = 0

GAME_ENEMIES: dict[EnemyID : GameEnemy] = {
    EnemyID.LARGE_RAT : GameEnemy(EnemyID.LARGE_RAT, name='Large Rat', desc= 'A rat the size of a large dog',
                              ascii='R', maxHealth=5, atk=2, deff=0, xp=10, gold=2)
}

def getEnemy(id: int) -> GameEnemy:
    return GAME_ENEMIES.get(EnemyID(id))
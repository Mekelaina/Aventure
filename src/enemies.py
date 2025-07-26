from enum import IntEnum
from aventure_enemy import *

class EnemyID(IntEnum):
    NO_ENEMY = 0 # dummy enemy that isnt actually an enemy. but marks no enemey
    LARGE_RAT = 1

GAME_ENEMIES: dict[EnemyID : GameEnemy] = {
    EnemyID.NO_ENEMY : GameEnemy(EnemyID.NO_ENEMY, name='', desc='', ascii='', maxHealth=0,
                                 atk=0, deff=0, xp=0, gold=0),
    EnemyID.LARGE_RAT : GameEnemy(EnemyID.LARGE_RAT, name='Large Rat', desc= 'A rat the size of a large dog',
                              ascii='R', maxHealth=5, atk=2, deff=0, xp=10, gold=2)
}

def getEnemy(id: int) -> GameEnemy:
    return GAME_ENEMIES.get(EnemyID(id))
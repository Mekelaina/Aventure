from enum import IntEnum
from aventure_enemy import *

class EnemyID(IntEnum):
    NO_ENEMY = 0 # dummy enemy that isnt actually an enemy. but marks no enemey
    LARGE_RAT = 1,
    RABID_RAT = 2,
    RAT_KING = 3,
    ZOMBIE_RAT = 4,
    WIZARD_RAT = 5

GAME_ENEMIES: dict[EnemyID : GameEnemy] = {
    EnemyID.NO_ENEMY : GameEnemy(EnemyID.NO_ENEMY, name='', desc='', ascii='', maxHealth=0,
                                 atk=0, deff=0, xp=0, gold=0),
    EnemyID.LARGE_RAT : GameEnemy(EnemyID.LARGE_RAT, name='Large Rat', desc= 'A rat the size of a large dog',
                              ascii='L', maxHealth=5, atk=2, deff=0, xp=10, gold=2),
    EnemyID.RABID_RAT: GameEnemy(EnemyID.RABID_RAT, name='Rabid Rat', desc='A Large rat with a foamed mouth, best stay clear',
                                 ascii='R', maxHealth=5, atk=3, deff=1, xp=15, gold=2),
    EnemyID.RAT_KING: GameEnemy(EnemyID.RAT_KING, 'Rat King', 'He\'s the giant rat that makes all of da rules!',
                                'K', 10, 5, 2, 100, 100),
    EnemyID.ZOMBIE_RAT: GameEnemy(EnemyID.ZOMBIE_RAT, 'Zombie Rat', 'An undead rat with rotten flesh.',
                                'Z', 4, 2, 4, 20, 0),
    EnemyID.WIZARD_RAT: GameEnemy(EnemyID.WIZARD_RAT, 'Wizard Rat', 'A wise looking rat in a pointed hat with a long, matted beard.',
                                  ascii='W', maxHealth=10, atk=10, deff=10, xp=10, gold=10)
    

}
async def getEnemy(id: int) -> GameEnemy:
    return GAME_ENEMIES.get(EnemyID(id))
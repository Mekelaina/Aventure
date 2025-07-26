from aventure_player import Player, GameState
from maps import getMap, MapID
from aventure_map import Room, Map, Direction, Door
from aventure_enemy import *
from enemies import getEnemy, EnemyID
from ascii_bulder import buildRoom


def checkForBattle(map: Map, player: Player) -> bool:
    room = map.rooms[player.data.room]
    if room.hasEnemies:
        return True
    return False

def move(player: Player, d: Door):
    
    if not d.open:
        if d.next == -1:
            print('Thats a wall..')
        else:
            print('the door is locked')
    else:
        if d.next == -1:
            print('The floor behind the door is gone. its just a void')
        else:
            player.data.room = d.next
    return False

class Game:
    def __init__(self):
        self.player: Player = Player()
        self.map: Map = Map(-1, [])
        self.enemy: GameEnemy = GameEnemy()
    
    def loadGame(self):
        pass

    def saveGame(self):
        pass

    def newGame(self, mapID: MapID):
        self.player.restart(mapID)
        



def debug():
    player: Player = Player()
    enemy: GameEnemy = getEnemy(EnemyID.NO_ENEMY)
    gmap: Map = getMap(0)
    
    




debug()
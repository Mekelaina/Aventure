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

def debug():
    player: Player = Player()
    player.data.map = 0
    player.data.room = 0
    player.state = GameState.RUN_DUNGEON
    enemy: GameEnemy = getEnemy(EnemyID.LARGE_RAT)
    gmap: Map = getMap(0)
    loop: bool = True

    res = buildRoom(gmap.rooms[0])

    print(res)
    
    
    # # print(f'A {enemy.name} attacks!')
    # # print('------ fight! ------')
    # # print(f'Enemy HP: {enemy.currHealth}/{enemy.maxHealth}')
    # # print(f'Your HP: {player.data.currHealth}/{player.data.maxHealth}')
    # while loop:
        
    #     text = input('>')
    #     tokens = text.split()
    #     l: dict[Direction, Door] = gmap.rooms[player.data.room].layout
    #     match player.state:
    #         case GameState.RUN_DUNGEON:
    #             print(f'Room {player.data.room}')
    #             match text:
    #                 case 'q':
    #                     loop = False
    #                 case 'n':
    #                     move(player, l[Direction.NORTH])
    #                 case 's':
    #                     move(player, l[Direction.SOUTH])
    #                 case 'e':
    #                     move(player, l[Direction.EAST])
    #                 case 'w':
    #                     move(player, l[Direction.WEST])
    #                 case _:
    #                     print(f'Unrecognized input: {text}')
    #         case GameState.RUN_COMBAT:
                
    #             match text:
    #                 case 'a':
    #                     enemy.takeDamage(player.getAttack())
    #                     player.takeDamage(enemy.atk)
                        
    #                 case 'd':
    #                     print('no def implemented')
    #                 case _:
    #                     print(f'Unrecognized input: {text}')
    #             print(f'Alive: {enemy.isAlive}')
    #             print(f'Enemy HP: {enemy.currHealth}/{enemy.maxHealth}')
    #             print(f'Your HP: {player.data.currHealth}/{player.data.maxHealth}')



debug()
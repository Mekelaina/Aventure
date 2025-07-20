from aventure_player import Player
from maps import getMap
from aventure_map import Room, Map, Direction, Door

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

def debug():
    player: Player = Player()
    player.data.map = 0
    player.data.room = 0
    gmap: Map = getMap(0)
    loop: bool = True
    
    while loop:
        print(f'Room {player.data.room}')
        text = input('>')
        l: dict[Direction, Door] = gmap.rooms[player.data.room].layout
        match text:
            case 'q':
                loop = False
            case 'n':
                move(player, l[Direction.NORTH])
            case 's':
                move(player, l[Direction.SOUTH])
            case 'e':
                move(player, l[Direction.EAST])
            case 'w':
                move(player, l[Direction.WEST])


debug()
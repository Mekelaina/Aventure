from aventure_map import Room, Direction
NS_LOCKED = '-'
UNLOCKED = '*'
WALL = '#'
EW_LOCKED = '|'
SWITCH = '%'
TREASURE = '$'
PLAYER = '@'
SPACE = ' '
COL: int = 13
ROW: int = 6

       

# this function returns an ascii depiction of the room from the provided
# room and direction the player entered from

def build( room: Room, enter: Direction = Direction.NORTH):
    buff: list[str] = [[SPACE for i in range(COL)] for j in range(ROW)] 
    if room.id == 0:
        buff[int(ROW/2)-1][int((COL-1)/2)] = PLAYER
        for i, x in room.layout.items():
            match i:
                case Direction.NORTH:
                    if x.next != -1:
                        pass
                    else:
                        pass
                case Direction.SOUTH:
                    print('south')
                case Direction.EAST:
                    print('east')
                case Direction.WEST:
                    print('west')
    else:
        pass
    
    res = ''
    for i in range(ROW):
        for j in range(COL):
            res += buff[i][j]
        res += '\n'
    return res
    #for i in bu
    # if room.id == 0:
    #     buff[(self.ROW/2)-1][(self.COL-1)/2] = self.PLAYER
    #     for dir in Direction:
    #         match dir:
    #             case Direction.NORTH:
    #                 for i in range(self.COL):
    #                     buff[][]
    #             case Direction.SOUTH:
    #                 pass
    #             case Direction.EAST:
    #                 pass
    #             case Direction.WEST:
    #                 pass
    # else:
    #     pass
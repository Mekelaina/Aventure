from aventure_map import Room, Direction
from enemies import getEnemy
NS_LOCKED = '-'
UNLOCKED = '*'
WALL = '#'
EW_LOCKED = '|'
SWITCH = '%'
SWITCH_TOGGLED = '/'
TREASURE = '$'
PLAYER = '@'
SPACE = ' '
# COL is characters per row
COL: int = 13
#ROW is lines
ROW: int = 6

COL_MID: int = 6
ROW_MID: int = 2

#Door index used for substituting WALL chars with Locked/Unlocked door chars
#recalculate if ROW/COL changes!!!

#start index for N/S Doors
NS_DOOR_START: int = 4
#end index for N/S Doors
NS_DOOR_END: int = 8
#start index for E/W Doors
EW_DOOR_START: int = 2
#end index for E/W Doors
EW_DOOR_END: int = 3

       

# this function returns an ascii depiction of the room from the provided
# room and direction the player entered from

def buildRoom( room: Room, moved: bool, enter: Direction = Direction.NORTH):
    buff: list[str] = [[SPACE for i in range(COL)] for j in range(ROW)] 
    
    for i, x in room.layout.items():
        match i:
            case Direction.NORTH:
                if x.next != -1: 
                    if x.open:
                        for c in range(COL):
                            if c >= 4 and c <= 8:
                                buff[0][c] = UNLOCKED
                            else:
                                buff[0][c] = WALL
                    else:
                        for c in range(COL):
                            if c >= 4 and c <= 8:
                                buff[0][c] = NS_LOCKED
                            else:
                                buff[0][c] = WALL
                else:
                    for c in range(COL):    
                        buff[0][c] = WALL
#================ end North ================
            case Direction.SOUTH:
                if x.next != -1: 
                    if x.open:
                        for c in range(COL):
                            if c >= NS_DOOR_START and c <= NS_DOOR_END:
                                buff[ROW-1][c] = UNLOCKED
                            else:
                                buff[ROW-1][c] = WALL
                    else:
                        for c in range(COL):
                            if c >= NS_DOOR_START and c <= NS_DOOR_END:
                                buff[ROW-1][c] = NS_LOCKED
                            else:
                                buff[ROW-1][c] = WALL
                else:
                    for c in range(COL):    
                        buff[ROW-1][c] = WALL
#================ end South ================
            case Direction.EAST:
                if x.next != -1: 
                    if x.open:
                        for c in range(ROW):
                            if c >= EW_DOOR_START and c <= EW_DOOR_END:
                                buff[c][COL-1] = UNLOCKED
                            else:
                                buff[c][COL-1] = WALL
                    else:
                        for c in range(ROW):
                            if c >= EW_DOOR_START and c <= EW_DOOR_END:
                                buff[c][COL-1] = EW_LOCKED
                            else:
                                buff[c][COL-1] = WALL
                else:
                    for c in range(ROW):    
                        buff[c][COL-1] = WALL
#================ end East ================
            case Direction.WEST:
                if x.next != -1: 
                    if x.open:
                        for c in range(ROW):
                            if c >= EW_DOOR_START and c <= EW_DOOR_END:
                                buff[c][0] = UNLOCKED
                            else:
                                buff[c][0] = WALL
                    else:
                        for c in range(ROW):
                            if c >= EW_DOOR_START and c <= EW_DOOR_END:
                                buff[c][0] = EW_LOCKED
                            else:
                                buff[c][0] = WALL
                else:
                    for c in range(ROW):    
                        buff[c][0] = WALL
#================ end West ================

    if room.id == 0 and not moved:
        buff[int(ROW/2)-1][int((COL-1)/2)] = PLAYER
    else:
        #NB: enter is the last moved direction, meaning
        #player is drawn from that directions opposite
        match enter:
            case Direction.NORTH:
                buff[ROW-2][COL_MID] = PLAYER
            case Direction.SOUTH:
                buff[1][COL_MID] = PLAYER
            case Direction.EAST:
                buff[ROW_MID][2] = PLAYER
            case Direction.WEST:
                buff[ROW_MID][COL-3] = PLAYER
        
        if room.hasEnemies:
            e = getEnemy(room.enemies[0]).ascii
            buff[int(ROW/2)-1][int((COL-1)/2)] = e
        
        if room.hasSwitch:
            # a bit confusing at first, basically
            #set this char to untoggle switch if switchToggled is false
            #otherwise set it to toggled switch
            buff[1][COL-3] = SWITCH if not room.switchToggled else SWITCH_TOGGLED
        if room.hasLoot:
            buff[ROW-2][2] = TREASURE

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
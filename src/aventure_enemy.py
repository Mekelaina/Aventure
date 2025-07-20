import copy

class GameEnemy():
    def __init__(self, id: int=0, name: str ='', desc: str='', ascii: str = '&', maxHealth=1,
                 atk: int = 2, deff: int = 0, xp: int = 0, gold: int = 0):
        self.id: int = id
        self.name: str = name
        self.desc: str = desc
        self.ascii: str = ascii
        self.maxHealth: int = maxHealth
        self.currHealth: int = maxHealth
        self.isAlive: bool = True
        self.atk: int = atk
        self.deff: int = deff
        self.expDrop: int = xp
        self.goldDrop: int = gold

    def takeDamage(self, amt: int):
        newHP = self.currHealth - amt
        if newHP > 0:
            self.currHealth = newHP
        else:
            self.currHealth = 0
            self.isAlive = False

    def newEnemy(self) -> 'GameEnemy':
        return copy.copy(self)
    
    def serialize(self) -> bytes:
        res = bytearray()
        res.extend(self.id.to_bytes())
        res.extend(self.isAlive.to_bytes())
        res.extend(self.currHealth.to_bytes())
        print(res)
        return bytes(res)
    
    def deserialize(self, blob: bytes) -> bool:
        if len(blob) != 3:
            return False
        else:
            self.id = blob[0]
            self.isAlive = bool(blob[1])
            self.currHealth = blob[2]
            return True

def debug():
    e = GameEnemy(2, maxHealth=10)
    print(f'e: {e.id}, {e.isAlive}, {e.currHealth}')
    print(e.serialize().hex())
    g = GameEnemy(2)
    g.deserialize(e.serialize())
    print(f'g: {g.id}, {g.isAlive}, {g.currHealth}')
debug()
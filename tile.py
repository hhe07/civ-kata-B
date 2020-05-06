from consts import TileType, TileProps, ProduceType, PlayerTag
from units import Army, Worker
#from eightcost import Army, Worker # Debugging purposes
class Tile:
    def __init__(self, loc: tuple):
        self.loc = loc
        self.x = loc[0]
        self.y = loc[1]
        self.resistance = 0
        self.food = 0
        self.prod = 0
        self.trade = 0
        self.owner = None
        self.tileType = TileType.FOW
        self.hasCity = False
        self.hasArmy = False
        self.hasWorkers = False
    
    def setOwner(self, owner: PlayerTag):
        """
        Sets the tile as being owned by a player.
        """
        self.owner = owner
    
    def setCity(self):
        """
        Sets the tile as having a city.
        """
        if not self.hasCity:
            self.hasCity = True
            self.resistance *= 1.5

    def addArmy(self):
        self.hasArmy = True
    
    def addWorkers(self):
        self.hasWorkers = True

    def hasArmies(self):
        """
        Checks if the tile has any armies
        """
        return self.hasArmy
    
    def hasWorkers(self):
        """
        Checks if the tile has any armies
        """
        return self.hasWorkers
    
    def setType(self, tt: TileType):
        """
        Sets the type of the tile. No need to set city prior.
        """
        self.tileType = tt
        if self.tileType != TileType.FOW:
            self.resistance = TileProps[self.tileType][0]
            if self.hasCity: self.resistance *= 1.5
            
            self.food = TileProps[self.tileType][1]
            self.prod = TileProps[self.tileType][2]
            self.trade = TileProps[self.tileType][3]
        del tt

    def hasType(self):
        return self.tileType != TileType.FOW
    
    def isDistAway(self, loc: tuple, dist: int = 2):
        """
        Checks whether a tile is within manhattan distance dist of current tile.
        WARN: Must be a viable location.
        """
        # TODO: Perhaps return deltaX+deltaY instead? or not?
        deltaX = abs(self.x - loc[0])
        deltaY = abs(self.y - loc[1])
        return (deltaX + deltaY <= dist)
    
    def getDistAway(self, dist: int = 2):
        """
        Gets tiles within manhattan distance dist of current tile.
        """
        ret = []
        minX = max(0, self.x - dist)
        minY = max(0, self.y - dist)
        maxX = min(32, self.x + dist + 1)
        maxY = min(32, self.y + dist + 1)  # 32 and + 1 due to range excluding last value
        for x in range(minX, maxX):
            for y in range(minY, maxY):
                loc = (x, y)
                if self.isDistAway(loc):
                    ret.append(loc)
        return ret
    
    def getPracResist(self):
        """
        Get practical resistance.
        """
        if self.hasArmies():
            return self.resistance
        else:
            return 0.0

    def getPracProd(self):
        """
        Gets practical production.
        """
        if self.hasWorkers():
            return self.prod
        else:
            return 0
    
    def isEnemy(self):
        """
        Determines whether current tile is occupied by enemy.
        """
        if self.tileType!=TileType.FOW:
            return (self.owner != PlayerTag.US)
        else:
            return None
"""
x = Tile((0, 0))

print(x.isEnemy())


print("resist")
# Resistance testing
x.setCity()
x.setType(TileType.FOREST)
print(x.getPracResist())
x.addArmy(Army())
print(x.getPracResist())


print("army")
# Armies testing
print(x.hasArmies())
x.removeArmy(Army())
print(x.hasArmies())


print("worker")
# Workers Testing
x.addWorkers(Worker())
print(x.hasWorkers())
print(x.getPracProd()) # Example for others - they're all the same
x.removeWorkers(Worker())
print(x.hasWorkers())
print(x.getPracProd())

print("owner")
# Ownership Testing
x.setOwner(PlayerTag.TA)
print(x.isEnemy())
x.setOwner(PlayerTag.US)
print(x.isEnemy())


print("dist")
# Distance Testing
print(x.isDistAway((2, 0)))
print(x.isDistAway((3, 0)))
print(x.getDistAway())
"""
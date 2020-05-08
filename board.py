from tile import Tile
from consts import PlayerTag, TileType
from command import Client
class Board:
    def __init__(self):
        self.allTiles = []
        for x in range(0, 32):
            row = []
            for y in range(0, 32):
                row.append(Tile((x, y)))
            self.allTiles.append(row)
        self.visible = []
    
    def getLoc(self, loc: tuple):
        """
        Returns Tile object associated with location loc
        """
        return self.allTiles[int(loc[0])][int(loc[1])]

    def updateType(self, board: list):
        """
        Updates tile types for all tiles
        """
        for x in range(0, 16):
            for y in range(0, 16):
                typ = TileType(board[x][y])
                self.getLoc((x, y)).setType(typ)
                self.getLoc((31 - x, y)).setType(typ)
                self.getLoc((x, 31 - y)).setType(typ)
                self.getLoc((31 - x, 31 - y)).setType(typ)
        
        
        posY = 0
        for row in board:
            posX = 0
            for item in row:
                if item!=-1:
                    self.visible.append((posX, posY))
                posX += 1
            posY += 1
    
    def updateCities(self, cities: list):
        """
        Updates city locations for all tiles
        """
        playert = 0
        for player in cities:
            for city in player:
                pos = (city["x"], city["y"])
                t = self.getLoc(pos)
                t.setOwner(PlayerTag(playert))
                t.setCity()
            playert+=1
        
    def updateArmies(self, armies: list):
        for row in self.allTiles:
            for t in row:
                t.hasArmy = False
        playert = 0
        for player in armies:
            for army in player:
                pos = (army["x"],army["y"])
                t = self.getLoc(pos)
                t.setOwner(PlayerTag(playert))
                t.addArmy()
                t.armyUnits.append(pos)
            playert += 1
        
    def updateWorkers(self, workers: list):
        for row in self.allTiles:
            for t in row:
                t.hasWorkers = False
        playert = 0
        for player in workers:
            for worker in player:
                pos = (worker["x"],worker["y"])
                t = self.getLoc(pos)
                t.setOwner(PlayerTag(playert))
                t.addWorkers()
            playert+=1

    def terrainResistance(self, pos: tuple, owners: list, dist: int = 2):
        """
        Gets terrain resistance with respect to surrounding tiles' owners.
        """
        tile = self.getLoc(pos)
        surrounding = tile.getDistAway(dist)
        resist = 0
        count = 0
        for loc in surrounding:
            t = self.getLoc(pos)
            if t.owner in owners:
                resist += t.resistance
                count += 1
        resist = resist / float(count)
        return resist - tile.resistance
    
    def highestValueSurrounding(self, pos: tuple, owners: list, dist: int = 2):
        """
        Gets highest value surrounding tile owned by owners.
        """
        tile = self.getLoc(pos)
        surrounding = tile.getDistAway(dist)
        highestVal = [tile]
        for loc in surrounding:
            t = self.getLoc(loc)
            if t.owner in owners:
                score = t.getResScore()
                tp = highestVal[0]
                prevScore = tp.getResScore()
                if score > prevScore:
                    highestVal = [t]
                if score == prevScore:
                    highestVal.append(t)
        return highestVal
    
    def calcHP(self, attackedTile: tuple, depth: int, myOff: float, theirDef: float):
        """
        Calculates HP lost in total for you and opponent when attacking tile. 
        Assumes all surrounding armies are used to attack, and all surrounding armies used to defend.
        """
        attackingArmies = []
        defendingArmies = []
        tile = self.getLoc(attackedTile)
        for surTileTup in tile.getDistAway(1):
            surTile = self.getLoc(surTileTup)
            if surTile.hasArmies():
                if surTile.owner == PlayerTag.US:
                    attackingArmies.extend(surTile.armyUnits)
                else:
                    defendingArmies.extend(surTile.armyUnits)
        attackingDmg = 0
        for x in attackingArmies:
            """
            Attacking damage calculation
            """
            attackingDmg += (myOff / theirDef) * 1 * len(tile.armies) * (self.getLoc(x).resistance / tile.resistance)
        return attackingDmg

    def isSaturated(self, tile: tuple):
        surr = self.getLoc(tile).getDistAway()
        isSaturated = 0
        for loc in surr:
            if self.getLoc(loc).hasWorkers or self.getLoc(loc).hasCity:
                isSaturated += 1
        return isSaturated == len(surr)
    
    def isFullDet(self, tile: tuple):
        surr = self.getLoc(tile).getDistAway()
        isDet = 0
        for loc in surr:
            if not self.getLoc(loc).hasWorkers and not self.getLoc(loc).hasCity:
                isDet +=1
        return isDet == len(surr)

    def getUnfilledWork(self, tile: tuple):
        ret = []
        surr = self.getLoc(tile).getDistAway()
        for loc in surr:
            t = self.getLoc(loc)
            if not t.hasWorkers:
               ret.append((t.getResScore(), tile, loc))
        return ret
    
    def getPossibleCities(self):
        ret = []
        for loc in self.visible:
            if self.isFullDet(loc):
                # TODO: Potential for possible tiles that aren't fully away?
                ret.append((self.terrainResistance(loc, [PlayerTag.US, None]), loc))
        ret.sort(key=lambda x: x[0], reverse=True)
        return ret

    def enemyClose(self, tile: tuple, dist: int = 3):
        surr = self.getLoc(tile).getDistAway(dist)
        for t in surr:
            l = self.getLoc(t)
            if l.owner != PlayerTag.US and l.owner != None:
                return True

    def enemyCityClose(self, tile: tuple, dist: int = 3):
        close = []
        surr = self.getLoc(tile).getDistAway(dist)
        for t in surr:
            l = self.getLoc(t)
            if l.owner != PlayerTag.US and l.owner != None and l.hasCity:
                close.append(t)
        return close
        
            

"""            
cl = Client("secret0", "http://localhost:8080")
b = Board()
x = cl.getBoard()
b.updateType(x["board"])
b.getLoc((0,0))
"""
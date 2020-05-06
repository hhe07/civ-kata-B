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
        
        posX = 0
        posY = 0
        for row in board:
            for item in row:
                if item!=-1:
                    self.visible.append((posX, posY))
                posX += 1
            posY += 1
        
    
    def updateCities(self, cities: list):
        """
        Updates city locations for all tiles
        """
        playerCount = 0
        for player in cities:
            for city in player:
                self.allTiles[city["x"]][city["y"]].setOwner(PlayerTag(playerCount))
                self.allTiles[city["x"]][city["y"]].setCity()
            playerCount += 1
        
    def updateArmies(self, armies: list):
        for row in self.allTiles:
            for t in row:
                t.hasArmy = False
        for army in armies:
            pos = army.currPos
            t = self.getLoc(pos)
            t.addArmy()
        # TODO: Armies reset - not safe, also army names are pizdec
    
    def updateWorkers(self, workers: list):
        for row in self.allTiles:
            for t in row:
                t.hasArmy = False
        for worker in workers:
            pos = worker.currPos
            t = self.getLoc(pos)
            t.addArmy()

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
                score = t.prod + t.food + t.trade
                tp = highestVal[0]
                prevScore = tp.prod + t.food + t.trade
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
                    attackingArmies.extend(surTile.armies)
                else:
                    defendingArmies.extend(surTile.armies)
        attackingDmg = 0
        for x in attackingArmies:
            """
            Attacking damage calculation
            """
            attackingDmg += (myOff / theirDef) * 1 * len(tile.armies) * (x.currTileResist / tile.resistance)
        for y in defendingArmies:
            """
            Calculates HP lost by counterattack
            """
            # TODO: Implement
            pass
        return attackingDmg


"""            
cl = Client("secret0", "http://localhost:8080")
b = Board()
x = cl.getBoard()
b.updateType(x["board"])
b.getLoc((0,0))
"""
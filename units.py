class unitBase:
    def __init__(self):
        self.currPos = None
        self.destination = None
    
    def setPos(self, pos: tuple):
        self.currPos = pos
    
    def getNext(self):
        deltaX = self.currPos[0] - self.destination[0]
        deltaY = self.currPos[1] - self.destination[1]
        xChange = (-1 * deltaX) / abs(deltaX)
        yChange = (-1 * deltaY) / abs(deltaY)
        return (self.currPos[0] + xChange, self.currPos[1] + yChange)
    
    def setDestination(self, pos: tuple):
        self.destination = pos
    
    def atDestination(self):
        return self.currPos == self.destination

class Worker(unitBase):
    def __init__(self):
        super().__init__(tag)
    
class Army(unitBase):
    def __init__(self):
        super().__init__()
        self.hp = 100
        self.currTileResist = 0
    
    def updateHP(self, hp: int):
        self.hp = hp

    def updateRes(self, res: float):
        self.currTileResist = res

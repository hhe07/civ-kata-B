class unitBase:
    def __init__(self, dest: tuple, currPos: tuple):
        self.currPos = currPos
        self.dest = dest
    
    def setPos(self, pos: tuple):
        self.currPos = pos
    
    def setDest(self, pos: tuple):
        self.dest = pos
    
    def getNext(self):
        deltaX = self.currPos[0] - self.dest[0]
        deltaY = self.currPos[1] - self.dest[1]
        if deltaX !=0:
            xChange = (-1 * deltaX) / abs(deltaX)
            yChange = 0
        else:
            xChange = 0
            if deltaY != 0:
                yChange = (-1 * deltaY) / abs(deltaY)
            else:
                yChange = 0
        return (int(self.currPos[0] + xChange), int(self.currPos[1] + yChange))
    
    def atDestination(self):
        return self.currPos == self.dest

class Worker(unitBase):
    def __init__(self, dest: tuple, currPos: tuple):
        super().__init__(dest, currPos)
    
class Army(unitBase):
    def __init__(self, dest: tuple, currPos: tuple):
        super().__init__(dest, currPos)
        self.hp = 100
        self.currTileResist = 0
    
    def updateHP(self, hp: int):
        self.hp = hp

    def updateRes(self, res: float):
        self.currTileResist = res

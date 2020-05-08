from consts import TileType, ProduceType, PlayerTag, TileProps
from units import Army, Worker
class Player:
    def __init__(self, tag: PlayerTag):
        self.tag = tag
        self.prevProd = 0
        self.prevTrade = 0
        self.food = 0
        self.production = 0
        self.trade = 0
        self.defense = 0.0
        self.offense = 0.0
        self.worstPossibleEight = 0
        self.worstPossibleCities = 0
        self.armies = []
        self.armyIds = []
        self.workers = []
        self.cities = []
        self.units = 0

    def updateRes(self, resources: dict):
        self.prevProd = self.production
        self.prevTrade = self.trade
        self.food = resources["food"]
        self.production = resources["production"]
        self.trade = resources["trade"] # TODO: Is tracking trade pointless?    
        if self.prevProd - self.production >= 8:
            self.worstPossibleEight += (self.production-(self.production % 8)) / 8
            if self.prevProd - self.production >= 24:
                self.worstPossibleCities += (self.production - (self.production % 24)) / 8
    
    def updateCities(self, cities: list):
        self.cities = []
        for city in cities:
            loc = (city["x"],city["y"])
            self.cities.append(loc)
    def updateBuffs(self, buffs: dict):
        self.defense = buffs["defense"]
        self.offense = buffs["offense"]
    
    def getMaxSustain(self):
        return max(self.food, 0)

    def canSmallConstr(self):
        return (self.production >= 8) and (self.getMaxSustain() > len(self.armies) + len(self.armies))
    
    def canLargeConstr(self):
        return (self.production >= 24)
    
    def canTradeConstr(self):
        return (self.trade >= 20)
    
    def updateArmies(self, armies: list):
        self.armies = []
        idGen = 0
        # TODO: Works for now, maybe use method of keeping track next position, and then updating position in object?
        for unconv in armies:
            tmp = Army()
            if tmp not in self.armies:
                tmp.setPos((unconv["x"],unconv["y"]))
                self.armies.append(tmp)
    
    def updateWorkers(self, workers: list):
        self.workers = []
        idGen = 0
        # TODO: Works for now, maybe use method of keeping track next position, and then updating position in object?
        for unconv in workers:
            tmp = Worker()
            if tmp not in self.workers:
                tmp.setPos((unconv["x"],unconv["y"]))
                self.workers.append(tmp)
                

#x = Player(PlayerTag.US)
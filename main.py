from command import Client
from player import Player
from consts import TileType, ProduceType, PlayerTag, TileProps, TechType
from units import Army, Worker
from tile import Tile
from board import Board

def __main__(name: str, key: str, url: str):
    cl = Client(key, url)
    cl.setName(name)
    board = Board()
    players = [Player(PlayerTag.US), Player(PlayerTag.TA), Player(PlayerTag.TB), Player(PlayerTag.TC)]

    while True:
        newBoard = cl.getBoard()
        newCities = cl.getCities()
        newArmies = cl.getArmies()
        newWorkers = cl.getWorkers()
        newRes = cl.getResources()
        newBuffs = cl.getPlayers()

        board.updateType(newBoard["board"])
        board.updateCities(newCities["cities"])
        board.updateArmies(newArmies["armies"])  # TODO: Non-functional
        board.updateWorkers(newWorkers["workers"])  # TODO: Non-functional
        
        playerCount = 0
        for player in players:
            player.updateRes(newRes["resources"][playerCount])
            player.updateBuffs(newBuffs["players"][playerCount])
            #player.updateArmies(newArmies["armies"][playerCount], PlayerTag(playerCount))
            #player.updateWorkers(newWorkers["workers"][playerCount], PlayerTag(playerCount))
            player.updateCities(newCities["cities"][playerCount])
            playerCount += 1
        if cl.getCurrentTurn()["turn"] == 0:
            if players[0].canSmallConstr():
                if players[0].canTradeConstr():
                    tradeAvailable = players[0].trade
                    while tradeAvailable >=20:
                        cl.produceTech(TechType.OFFENSE)
                        tradeAvailable -= 20
                        if tradeAvailable >= 20:
                            cl.produceTech(TechType.DEFENSE)
                            tradeAvailable -= 20                

                prodAvailable = players[0].production
                foodAvailable = players[0].getMaxSustain()
                

                needsSaturation = []
                saturated = []
                for city in players[0].cities:
                    if board.isSaturated(city):
                        saturated.append(city)
                    else:
                        needsSaturation.append(city)

                potentialWorkerBuilds = []  # Base number of workers to build off of this
                for req in needsSaturation:
                    potentialWorkerBuilds.extend(board.getUnfilledWork(req))
                
                potentialWorkerBuilds = list(dict.fromkeys(potentialWorkerBuilds))
                potentialWorkerBuilds.sort(key=lambda x: x[0], reverse=True)
                if len(saturated) == len(players[0].cities):
                    # If all cities saturated, start to build cities
                    # TODO: Update getPossibleCities after every build?
                    while prodAvailable >= 24 and players[0].units <= foodAvailable:
                        l = board.getPossibleCities()
                        cl.produce(ProduceType.CITY, l[0][1])
                        foodAvailable += board.getLoc(l[0][1]).food
                        prodAvailable -= 24
                        players[0].units += 1
                        
                    needsSaturation = []
                    for city in players[0].cities:
                        if not board.isSaturated(city):
                            needsSaturation.append(city)

                    for req in needsSaturation:
                        potentialWorkerBuilds.extend(board.getUnfilledWork(req))

                for t in potentialWorkerBuilds:
                    allWorkerLocs = [w.dest for w in players[0].workers]
                    if prodAvailable >= 8 and players[0].units <= foodAvailable and t[2] not in allWorkerLocs:
                        cl.produce(ProduceType.WORKER, t[1])
                        w = Worker(t[2], t[1])
                        players[0].workers.append(w)
                        foodAvailable += board.getLoc(t[2]).food
                        prodAvailable -= 8
                        players[0].units += 1
                if prodAvailable >= 8:
                    # If still production, throw armies at the problem until it sticks.
                    newPriorities = []
                    for city in players[0].cities:
                        if board.enemyClose(city) and prodAvailable >= 8 and players[0].units <= foodAvailable:
                            cl.produce(ProduceType.ARMY, city)
                            a = Army(city, city)
                            players[0].armies.append(a)
                            prodAvailable -= 8
                            players[0].units +=1
                

            for worker in players[0].workers:
                if not worker.atDestination():
                    newPos = worker.getNext()
                    cl.moveWorker(worker.currPos, newPos)
                    worker.setPos(newPos)
            
            for army in players[0].armies:
                newDestSet = False
                if not board.enemyClose(army.currPos):
                    for city in player[0].cities:
                        if board.enemyClose(city) and not newDestSet:
                            army.setDest(city)
                            newDestSet = True
                
                if len(board.enemyCityClose(army.currPos)) >= 1 and army.currPos in players[0].cities:
                    for city in board.enemyCityClose(army.currPos):
                        own = board.getLoc(city).owner.value
                        hplost = board.calcHP(city,3,players[0].offense, players[own].defense)
                        if army.hp - hplost > 0 and not newDestSet:
                            army.setDest(city)
                            newDestSet = True

                if not army.atDestination():
                    newPos = army.getNext()
                    cl.moveArmy(army.currPos, newPos)
                    army.currPos = newPos
            
            cl.endTurn()
                
                    

if __name__ == "__main__":  
    __main__("o.O", "ahZai6ie", "https://codekata-civ.herokuapp.com/" )
    #__main__("b", "secret0", "http://localhost:8080")

    

# ahZai6ie
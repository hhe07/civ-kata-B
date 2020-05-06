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
        board.updateArmies(players[0].armies)  # TODO: Non-functional
        board.updateWorkers(players[0].workers)  # TODO: Non-functional
        
        playerCount = 0
        for player in players:
            player.updateRes(newRes["resources"][playerCount])
            player.updateBuffs(newBuffs["players"][playerCount])
            player.updateArmies(newArmies["armies"][playerCount])
            player.updateWorkers(newWorkers["workers"][playerCount])
            player.updateCities(newCities["cities"][playerCount])
            playerCount += 1
        if cl.getCurrentTurn()["turn"] == 0:
            if not players[0].canSmallConstr():
                cl.endTurn()
            else:
                if players[0].canTradeConstr():
                    cl.produceTech(TechType.DEFENSE)
                # TODO: Figure out how to prioritise building cities, workers, armies
                # TODO: Convert enums into numbers prior to API req?
                prodAvailable = players[0].production
                
                saturated = 0
                
                for city in players[0].cities:
                    workerCount = 0
                    c = board.getLoc(city)
                    for pos in c.getDistAway():
                        if board.getLoc(pos).hasWorkers:
                            workerCount += 1
                    if workerCount == len(c.getDistAway()): saturated+=1

                if saturated > 0:
                    opts = [(0)]
                    for pos in board.visible:
                        t = board.getLoc(pos)
                        if not t.hasCity and t.hasWorkers:
                            score = t.prod + t.food + t.trade
                            score *= board.terrainResistance(pos, [PlayerTag.US, None])
                            if opts[0][0] < score:
                                opts = [(score, pos)]
                            elif opts[0][0] == score:
                                opts.append((score, pos))
                    ourProd = players[0].production
                    x = 0
                    while x < ((ourProd - ourProd % 24) / 24) and x < len(opts) and x < saturated:
                        if len(opts[x]) == 2:
                            cl.produce(ProduceType.CITY, opts[x])
                            prodAvailable -= 24
                            x+=1

                if prodAvailable >= 8:
                    options = []
                    # Get all tiles without workers
                    for city in players[0].cities:
                        surr = board.getLoc(city).getDistAway()
                        for loc in surr:
                            t = board.getLoc(loc)
                            if not t.hasWorkers:
                                score = t.food + t.prod + t.trade
                                options.append((score, loc, city))
                    options.sort(key=lambda x: x[0], reverse=True)
                    
                    x = 0
                    while x <= ((prodAvailable - prodAvailable % 8) / 8) and x <= len(options) and x <= round(len(players[0].armies) * 2):
                        cl.produce(ProduceType.WORKER, options[x][2])
                        # TODO: Actually add the bloody worker object in.
                        w = Worker()
                        w.setPos(options[x][2])
                        #print(options[x][1])
                        #print(options[x][2])
                        w.setDest(options[x][1])
                        print(w.dest)
                        players[0].workers.append(w)
                        prodAvailable -= 8
                        x += 1
                        
                    """
                    if prodAvailable >= 8:
                        options = []
                        for city in players[0].cities:
                            surr = board.getLoc(city).getDistAway()
                            for loc in surr:
                                score = board.terrainResistance(loc, [None, PlayerTag.US, PlayerTag.TA, PlayerTag.TB, PlayerTag.TC])
                                options.append((score, loc, city))
                        options.sort(key=lambda x: x[0], reverse=True)
                        
                        x = 0
                        while x < ((prodAvailable - prodAvailable % 8) / 8) and x < len(options) and prodAvailable > 0:
                            cl.produce(ProduceType.ARMY, options[x][2])
                            a = Army()
                            a.setPos(options[x][2])
                            a.setDestination(options[x][1])
                            players[0].armies.append(a)
                            prodAvailable -= 8
                            x += 1
                    """
                    cl.endTurn()

            for worker in players[0].workers:
                if not worker.atDestination():
                    newPos = worker.getNext()
                    cl.moveWorker(worker.currPos, newPos)
                    worker.currPos = newPos
            """
            for army in players[0].armies:
                if not army.atDestination():
                    newPos = army.getNext()
                    cl.moveArmy(army.currPos, newPos)
                    army.currPos = newPos
            """

                
                    

if __name__ == "__main__":  
    #__main__("dumpster fire", "ahZai6ie", "https://codekata-civ.herokuapp.com/" )
    __main__("b", "secret0", "http://localhost:8080")

    

# ahZai6ie
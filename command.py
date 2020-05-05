import requests, json
from consts import ProduceType, TechType
class Client:
    def __init__(self, key: str, url: str):
        self.url = url + "/api/"
        self.key = key
    
    def getTemplate(self, component: str):
        return json.loads(requests.get(self.url + component, params={"key": self.key}).text)

    def getBoard(self):
        return self.getTemplate("board")

    def getCities(self):
        return self.getTemplate("cities")

    def getArmies(self):
        return self.getTemplate("armies")
    
    def getWorkers(self):
        return self.getTemplate("workers")
    
    def getResources(self):
        return self.getTemplate("resources")
    
    def getCurrentTurn(self):
        return self.getTemplate("current_player")

    def getPlayers(self):
        return self.getTemplate("players")
    
    def getPlayerIndex(self):
        return self.getTemplate("player_index")

    def produce(self, typ: ProduceType, srcTup: tuple):
        params = {"key": self.key, "type": typ.value, "x": srcTup[0], "y": srcTup[1]}
        x = json.loads(requests.post(self.url + "produce", params=params).text)
        assert x["error"] == None
    
    def produceTech(self, techType: TechType):
        params = {"key": self.key, "technology": techType.value}
        requests.post(self.url+"technology", params = params)

    def moveWorker(self, srcTup: tuple, toTup: tuple):
        params = {"key": self.key, "srcX": srcTup[0], "srcY": srcTup[1], "dstX": toTup[0], "dstY": toTup[1]}
        x = json.loads(requests.post(self.url + "move_worker", params=params).text)
    
    def moveArmy(self, srcTup: tuple, toTup: tuple):
        params = {"key": self.key, "srcX": srcTup[0], "srcY": srcTup[1], "dstX": toTup[0], "dstY": toTup[1]}
        requests.post(self.url + "move_Army", params=params)
    
    def endTurn(self):
        requests.post(self.url + "end_turn", params={"key": self.key})

    def setName(self, name: str):
        requests.post(self.url + "set_name", params={"key": self.key, "name": name})
"""
x = Client("secret0","http://localhost:8080")
print(x.getPlayerIndex())
"""
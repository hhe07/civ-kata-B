from enum import Enum
class TileType(Enum):
    OCEAN = 0
    GRASSLAND = 1
    HILLS = 2
    FOREST = 3
    MOUNTAINS = 4
    FOW = -1

class ProduceType(Enum):
    ARMY = 0
    WORKER = 1
    CITY = 2

class TechType(Enum):
    OFFENSE = 0
    DEFENSE = 1

class PlayerTag(Enum):
    US = 0
    TA = 1
    TB = 2
    TC = 3

# Stored in order: (Resistances, Food, Production, Trade)
TileProps = {
    TileType.OCEAN: (0.5, 1, 0, 2),
    TileType.GRASSLAND: (1.0, 2, 1, 0),
    TileType.HILLS: (1.5, 2, 2, 1),
    TileType.FOREST: (1.5, 2, 3, 0),
    TileType.MOUNTAINS: (2.0, 1, 1, 0)
}

class defPriority(Enum):
    LOW = 0
    MED = 1
    HIGH = 2
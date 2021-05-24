from enum import Enum

DEFAULT_RESOLUTION = {'height': 720, 'width': 1280}


class BuildingNames(Enum):
    CITY_HALL = 'city_hall'
    BARRACKS = 'barracks'
    ARCHERY_RANGE = 'archery_range'
    STABLE = 'stable'
    SIEGE_WORKSHOP = 'siege_workshop'
    BLACKSMITH = 'blacksmith'
    TAVERN = 'tavern'
    SHOP = 'shop'
    ALLIANCE_CENTER = 'alliance_center'
    ACADEMY = 'academy'
    STOREHOUSE = 'storehouse'
    TRADING_POST = 'trading_post'
    SCOUT_CAMP = 'scout_camp'
    COURIER_STATION = 'courier_station'
    BUILDERS_HUT = "builder's_hut"
    CASTLE = 'castle'
    HOSPITAL = 'hospital'
    FARM = 'farm'
    LUMBER_MILL = 'lumber_mill'
    QUARRY = 'quarry'
    GOLDMINE = 'goldmine'
    WALL = 'wall'


class TrainingType(Enum):
    UPGRADE = 'upgrade'
    UPGRADE_AND_TRAIN = 'upgrade_and_train'
    TRAIN = 'train'
    NO_ACTION = 'no_action'


class TaskName(Enum):
    KILL_GAME = -2
    BREAK = -1
    NEXT_TASK = 0
    INIT_BUILDING_POS = 1
    COLLECTING = 2
    CLAIM_QUEST = 3
    TRAINING = 4
    GATHER = 5
    ALLIANCE = 6
    METARIALS = 7
    TAVERN = 8
    VIP_CHEST = 9
    BARBARIANS = 10
    SCOUT = 11
    GATHER_GEM = 12
    MYSTERY_MERCHANT = 13


class Resource(Enum):
    FOOD = 0
    WOOD = 1
    STONE = 2
    GOLD = 3

from device_gui_detector import GuiName
from device_gui_detector import GuiDetector
from constants.file_relative_paths import ImagePathAndProps
from constants.file_relative_paths import FilePaths
from datetime import datetime
from utils import aircv_rectangle_to_box
from utils import resource_path
from enum import Enum

import math
import time
import json
import haoi


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


class TrainingAndUpgradeLevel(Enum):
    T1 = 0
    T2 = 1
    T3 = 2
    T4 = 3
    T5 = 4
    UPGRADE_ALL = 5
    DISABLED = -1


class TaskName(Enum):
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


class Resource(Enum):
    FOOD = 0
    WOOD = 1
    STONE = 2
    GOLD = 3


class Bot:

    def __init__(self, device, config={}):
        self.device = device
        self.gui = GuiDetector(device)
        self.text_update_event = lambda v: v
        self.text = {
            'title': '',
            'text_list': []
        }

        self.building_pos_update_event = lambda **kw: kw

        # get screen resolution
        str = device.shell('wm size').replace('\n', '')
        height, width = list(map(int, str[(str.find(':') + 1):len(str)].split('x')))
        self.resolution = {
            'height': height,
            'width': width
        }

        self.building_pos = {}

        self.config = BotConfig(config)
        self.curr_task = TaskName.BREAK

    def start(self, curr_task=TaskName.COLLECTING):

        if self.building_pos is None:
            curr_task=TaskName.INIT_BUILDING_POS

        while True:
            # 0 break
            if curr_task == TaskName.BREAK and self.config.enableBreak:
                self.set_text(title='Break', remove=True)
                self.set_text(insert='Init View')
                self.set_text(insert='0/{} seconds'.format(self.config.breakTime))
                self.back_to_home_gui()
                self.home_gui_full_view()
                count = 0
                for i in range(self.config.breakTime):
                    time.sleep(1)
                    count = count + 1
                    self.set_text(replace='{}/{} seconds'.format(count, self.config.breakTime), index=0)
                curr_task = TaskName.COLLECTING

            elif curr_task == TaskName.BREAK:
                curr_task = TaskName.COLLECTING

            # 1. init building position if need
            if not self.config.hasBuildingPos or curr_task == TaskName.INIT_BUILDING_POS:
                curr_task = self.init_building_pos()

            # 2.collecting resource
            if curr_task == TaskName.COLLECTING and self.config.enableCollecting:
                curr_task = self.collecting_soldiers_resources_and_help(TaskName.CLAIM_QUEST)
            elif curr_task == TaskName.COLLECTING:
                curr_task = TaskName.CLAIM_QUEST

            # 3.claim quests
            if curr_task == TaskName.CLAIM_QUEST and self.config.claimQuests:
                curr_task = self.claim_quests(TaskName.ALLIANCE)
            elif curr_task == TaskName.CLAIM_QUEST:
                curr_task = TaskName.ALLIANCE

            # 4.alliance
            if curr_task == TaskName.ALLIANCE and self.config.allianceAction:
                curr_task = self.alliance(TaskName.METARIALS)
            elif curr_task == TaskName.ALLIANCE:
                curr_task = TaskName.METARIALS

            # 5.material
            if curr_task == TaskName.METARIALS and self.config.enableMaterialProduce:
                curr_task = self.materials(TaskName.TAVERN)
            elif curr_task == TaskName.METARIALS:
                curr_task = TaskName.TAVERN

            # 6.tavern
            if curr_task == TaskName.TAVERN and self.config.enableTavern:
                curr_task = self.tavern(TaskName.TRAINING)
            elif curr_task == TaskName.TAVERN:
                curr_task = TaskName.TRAINING

            # 7.train soldiers
            if curr_task == TaskName.TRAINING and self.config.enableTraining:
                curr_task = self.training_and_upgrade(TaskName.GATHER)
            elif curr_task == TaskName.TRAINING:
                curr_task = TaskName.GATHER

            # 8.gather resource
            if curr_task == TaskName.GATHER and self.config.gatherResource:
                curr_task = self.gather_resource(TaskName.BREAK)
            elif curr_task == TaskName.GATHER:
                curr_task = TaskName.BREAK

        return

    # screen range x0 250, x1 950, y0 95, y1 615
    def init_building_pos(self, next_task=TaskName.COLLECTING):

        try:
            self.set_text(title='Init Building Position', remove=True)
            self.set_text(insert='init view')
            self.set_text(insert='progress: 0%', index=0)

            self.back_to_home_gui()
            self.home_gui_full_view()

            # close menu
            self.menu_should_open(False)

            if self.config.hasBuildingPos:
                self.curr_task = TaskName.NEXT_TASK
                return

            width = DEFAULT_RESOLUTION['width']
            height = DEFAULT_RESOLUTION['height']

            x0 = 250
            x1 = 950
            y0 = 95
            y1 = 615

            x_times = 12
            y_times = 10

            x_interval = math.floor((x1 - x0) / (x_times - 1))
            y_interval = math.floor((y1 - y0) / y_times)

            x_start = x0
            y_start = y0

            x_end = x1
            y_end = y1

            total = x_times * y_times

            # tap every point to get building position
            for row in range(0, y_times):
                for col in range(0, x_times):
                    x, y = x_start + x_interval * col, y_start + y_interval * row
                    self.tap(x, y, 1)
                    num_of_back = self.back_to_home_gui()
                    if num_of_back == 0:
                        self.tap(x_start, y_start)
                        self.tap(x, y)

                    # sleep 0.5 sec just for a case if screen print before button display
                    time.sleep(0.5)
                    # check is tap on building
                    result = self.gui.has_image(ImagePathAndProps.BUILDING_INFO_BUTTON_IMG_PATH.value)

                    # if tap on the building, then try to tap on building infomation button to get building name
                    if result is not None:
                        self.tap(result['result'][0], result['result'][1], 1)
                        name = self.gui.get_windows_name()
                        if name is None:
                            self.back_to_home_gui()
                        else:
                            name = name.lower()
                            level = 0
                            if 'level ' in name:
                                level, name = name.replace('level ', '').split(' ', 1)
                            self.building_pos[name.replace(' ', '_')] = (x, y)
                            # bot_print("Building <{}> on position ({}, {}) ".format(name, x, y))
                            self.set_text(insert='Building <{}> on position ({}, {})'.format(name, x, y),index=1)
                            self.back()

                    self.tap(x_start, y_start)
                    self.set_text(
                        replace='progress: {}%'.format( int(((row * x_times) + (col + 1)) / total * 100)),
                        index=0)

                    # bot_print("{}/{}".format((row * x_times) + (col + 1), total))

            # save building pos to json
            self.building_pos_update_event(building_pos=self.building_pos, prefix=self.device.serial.replace(':', "_"))

        except Exception as e:
            return TaskName.INIT_BUILDING_POS
        return next_task

    def collecting_soldiers_resources_and_help(self, next_task=TaskName.CLAIM_QUEST):
        self.set_text(title='Collecting Resource, Troops, and Help Alliance', remove=True)
        self.set_text(insert='Init view')

        try:
            self.back_to_home_gui()
            self.home_gui_full_view()

            self.menu_should_open(False)

            width = DEFAULT_RESOLUTION['width']
            height = DEFAULT_RESOLUTION['height']
            x_e, y_e = 105, 125
            for name in [
                BuildingNames.BARRACKS.value,
                BuildingNames.ARCHERY_RANGE.value,
                BuildingNames.STABLE.value,
                BuildingNames.SIEGE_WORKSHOP.value,
                BuildingNames.FARM.value,
                BuildingNames.LUMBER_MILL.value,
                BuildingNames.QUARRY.value,
                BuildingNames.GOLDMINE.value,
                BuildingNames.ALLIANCE_CENTER.value
            ]:
                x, y = self.building_pos[name]
                self.set_text(insert='tap building {} at position ({},{})'.format(name, x, y))
                self.tap(x, y)
                self.tap(x_e, y_e)

        except Exception as e:
            return TaskName.COLLECTING
        return next_task

    def claim_quests(self, next_task=TaskName.ALLIANCE):
        self.set_text(title='Claim Quest and Daily Objective', remove=True)
        try:
            self.back_to_home_gui()
            self.tap(45, 170, 5)

            quests_tap_pos = (100, 180)
            daily_objectives_tap_pos = (100, 320)

            self.set_text(insert='Claim quest')
            self.tap(quests_tap_pos[0], quests_tap_pos[1], 1)
            while True:
                result = self.gui.has_image(ImagePathAndProps.QUEST_CLAIM_BUTTON_IMAGE_PATH.value)
                if result is None:
                    break
                x, y = result["result"]
                self.set_text(insert='Tap claim button at ({}, {})'.format(x, y))
                self.tap(x, y, 0.5)

            self.set_text(insert='Claim Daily Objective')
            self.tap(daily_objectives_tap_pos[0], daily_objectives_tap_pos[1], 1)
            while True:
                result = self.gui.has_image(ImagePathAndProps.QUEST_CLAIM_BUTTON_IMAGE_PATH.value)
                if result is None:
                    break
                x, y = result["result"]
                self.set_text(insert='Tap claim button at ({}, {})'.format(x, y))
                self.tap(x, y, 0.5)

            self.set_text(insert='Tap all chest')
            # chest position
            for pos in [(355, 200), (530, 200), (710, 200), (885, 200), (1050, 200)]:
                self.tap(pos[0], pos[1], 0.3)
        except Exception as e:
            return TaskName.CLAIM_QUEST
        return next_task

    def alliance(self, next_tast=TaskName.METARIALS):
        self.set_text(title='Alliance', remove=True)
        allince_button_pos = (1030, 670)
        try:
            for name in ['GIFTS', 'TERRITORY', 'TECHNOLOGY']:
                self.set_text(insert='Open alliance')
                self.back_to_home_gui()
                self.menu_should_open(True)
                x, y = allince_button_pos
                self.tap(x, y, 3)
                if name == 'GIFTS':
                    self.set_text(insert='Claim gift')
                    gifts_pos = (885, 560)
                    rate_pos = (930, 205)
                    normal_pos = (670, 205)
                    claim_all_pos = (1110, 205)
                    x, y = gifts_pos
                    self.tap(x, y, 2)

                    # collecting rate gifts
                    self.set_text(insert='Claim rate gift')
                    x, y = rate_pos
                    self.tap(x, y, 1)
                    while True:
                        result = self.gui.has_image(ImagePathAndProps.GIFTS_CLAIM_BUTTON_IMAGE_PATH.value)
                        if result is None:
                            break
                        x, y = result['result']
                        self.tap(x, y, 0.5)

                    # collecting normal gifts
                    self.set_text(insert='Claim normal gift')
                    x, y = normal_pos
                    self.tap(x, y, 1)
                    x, y = claim_all_pos
                    self.tap(x, y, 1)

                elif name == 'TERRITORY':
                    self.set_text(insert='Claim resource')
                    territory_pos = (885, 405)
                    claim_pos = (1020, 140)
                    x, y = territory_pos
                    self.tap(x, y, 2)
                    x, y = claim_pos
                    self.tap(x, y, 1)

                elif name == 'TECHNOLOGY':
                    self.set_text(insert='Donate technology')
                    technologe_pos = (760, 560)
                    x, y = technologe_pos
                    self.tap(x, y, 5)
                    result = self.gui.has_image(ImagePathAndProps.TECH_RECOMMEND_IMAGE_PATH.value)
                    if result is not None:
                        x, y = result['result']
                        self.tap(x, y + 60, 1)
                        result = self.gui.has_image(ImagePathAndProps.TECH_DONATE_BUTTON_IMAGE_PATH.value)
                        if result is not None:
                            x, y = result['result']
                            for i in range(20):
                                self.tap(x, y, 0.03)
                    else:
                        self.set_text(insert="Cannot found Officer's Recommendation")

        except Exception as e:
            return TaskName.ALLIANCE
        return next_tast

    def materials(self, next_task=TaskName.TAVERN):
        self.set_text(title='Materials Production', remove=True)

        icon_pos = [
            (765, 230),
            (860, 230),
            (950, 230),
            (1045, 230)
        ]
        self.set_text(insert='Init view')
        self.back_to_home_gui()
        self.home_gui_full_view()
        blacksmith_pos = self.building_pos[BuildingNames.BLACKSMITH.value]
        x, y = blacksmith_pos
        self.tap(x, y, 2)
        result = self.gui.has_image(ImagePathAndProps.MATERIALS_PRODUCTION_BUTTON_IMAGE_PATH.value)
        if result is None:
            return next_task
        x, y = result['result']
        self.tap(x, y, 5)
        list_amount = self.gui.materilal_amount_image_to_string()
        self.set_text(insert='\nLeather: {}\nIton: {}\nEboy: {}\nBone: {}'.format(
            list_amount[0], list_amount[1], list_amount[2], list_amount[3])
        )
        min = 0
        for i in range(len(list_amount)):
            if list_amount[min] > list_amount[i]:
                min = i
        x, y = icon_pos[min]
        self.set_text(insert='Produce least material')
        for i in range(5):
            self.tap(x, y, 0.5)
        return next_task

    def tavern(self, next_task=TaskName.TRAINING):
        self.set_text(title='Tavern', remove=True)
        self.set_text(insert='Init view')
        self.back_to_map_gui()
        self.back_to_home_gui()
        self.home_gui_full_view()
        tavern_pos = self.building_pos[BuildingNames.TAVERN.value]

        # tap tavern building
        x, y = tavern_pos
        self.set_text(insert='Tap tavern at position ({}, {})'.format(x, y))
        self.tap(x, y, 1)
        result = self.gui.has_image(ImagePathAndProps.TAVERN_BUTTON_BUTTON_IMAGE_PATH.value)
        if result is None:
            return next_task
        x, y = result['result']
        self.tap(x, y, 4)
        while True:
            result = self.gui.has_image(ImagePathAndProps.CHEST_OPEN_BUTTON_IMAGE_PATH.value)
            if result is None:
                return next_task
            x, y = result['result']
            self.set_text(insert="Tap open button at ({}, {})".format(x, y))
            self.tap(x, y, 4)
            result = self.gui.has_image(ImagePathAndProps.CHEST_CONFIRM_BUTTON_IMAGE_PATH.value)
            if result is None:
                return next_task
            x, y = result['result']
            self.tap(x, y, 4)

    def training_and_upgrade(self, next_task=TaskName.GATHER):
        self.set_text(title='Train and Upgrade Troops', remove=True)
        self.set_text(insert='Init view')
        self.back_to_map_gui()
        self.back_to_home_gui()
        self.home_gui_full_view()
        try:
            soldier_icon_pos = [
                (630, 175),
                (730, 175),
                (830, 175),
                (930, 175),
                (1030, 175),
            ]

            for config in [
                [
                    ImagePathAndProps.BARRACKS_BUTTON_IMAGE_PATH.value,
                    self.config.trainBarracksTrainingLevel,
                    self.config.trainBarracksUpgradeLevel,
                    self.building_pos[BuildingNames.BARRACKS.value],
                    BuildingNames.BARRACKS.value,
                ],
                [
                    ImagePathAndProps.ARCHER_RANGE_BUTTON_IMAGE_PATH.value,
                    self.config.trainArcheryRangeTrainingLevel,
                    self.config.trainArcheryRangeUpgradeLevel,
                    self.building_pos[BuildingNames.ARCHERY_RANGE.value],
                    BuildingNames.ARCHERY_RANGE.value
                ],
                [
                    ImagePathAndProps.STABLE_BUTTON_IMAGE_PATH.value,
                    self.config.trainStableTrainingLevel,
                    self.config.trainStableUpgradeLevel,
                    self.building_pos[BuildingNames.STABLE.value],
                    BuildingNames.STABLE.value,
                ],
                [
                    ImagePathAndProps.SIEGE_WORKSHOP_BUTTON_IMAGE_PATH.value,
                    self.config.trainSiegeWorkshopTrainingLevel,
                    self.config.trainSiegeWorkshopUpgradeLevel,
                    self.building_pos[BuildingNames.SIEGE_WORKSHOP.value],
                    BuildingNames.SIEGE_WORKSHOP.value
                ]
            ]:
                self.set_text(insert='Train or upgrade troops({})'.format(config[4]))
                self.back_to_home_gui()
                upgraded = False
                x, y = config[3]
                self.tap(x, y, 1)
                result = self.gui.has_image(config[0])
                if result is None:
                    continue
                x, y = result['result']
                self.tap(x, y, 1)
                result = self.gui.has_image(ImagePathAndProps.SPEED_UP_BUTTON_IMAGE_PATH.value)
                if result is not None:
                    continue
                if config[2] != TrainingAndUpgradeLevel.DISABLED.value:
                    max = config[2] if config[2] != TrainingAndUpgradeLevel.UPGRADE_ALL.value \
                        else TrainingAndUpgradeLevel.T4.value
                    min = config[2] - 1 if config[2] != TrainingAndUpgradeLevel.UPGRADE_ALL.value else -1
                    for i in range(max, min, -1):
                        x, y = soldier_icon_pos[i]
                        self.tap(x, y, 0.5)
                        # check has upgrade button, if has then tap it
                        result = self.gui.has_image(ImagePathAndProps.TRAINING_UPGRADE_BUTTON_IMAGE_PATH.value)
                        if result is None:
                            if config[2] != TrainingAndUpgradeLevel.UPGRADE_ALL.value:
                                break
                            else:
                                continue
                        x, y = result['result']
                        self.set_text(insert='Upgrade T{}({})'.format(i+1, config[4]))
                        self.tap(x, y, 0.5)

                        # check has train button if has then tap it
                        result = self.gui.has_image(ImagePathAndProps.UPGRADE_BUTTON_IMAGE_PATH.value)
                        x, y = result['result']
                        self.tap(x, y, 0.5)
                        upgraded = True

                if not upgraded and (
                        config[1] != TrainingAndUpgradeLevel.DISABLED.value):
                    for i in range(config[1], -1, -1):
                        x, y = soldier_icon_pos[i]
                        self.tap(x, y, 0.5)
                        result = self.gui.has_image(ImagePathAndProps.TRAIN_BUTTON_IMAGE_PATH.value)
                        if result is None:
                            continue
                        self.set_text(insert='Train T{}({})'.format(i + 1, config[4]))
                        x, y = result['result']
                        self.tap(x, y, 0.5)
                        break
        except Exception as e:
            return TaskName.TRAINING
        return next_task

    def gather_resource(self, next_task=TaskName.BREAK):
        self.set_text(title='Gather Resource', remove=True)

        last_resource_pos = []
        resource_type = ''
        should_decreasing_lv = False
        resource_icon_pos = [
            (450, 640),
            (640, 640),
            (830, 640),
            (1030, 640)
        ]
        try:
            chose_icon_pos = resource_icon_pos[0]
            self.back_to_map_gui()
            resourse_code = self.get_min_resource()
            self.back_to_map_gui()

            if resourse_code == Resource.FOOD.value:
                chose_icon_pos = resource_icon_pos[0]
                self.set_text(insert="Search food")
                resource_type = 'food'

            elif resourse_code == Resource.WOOD.value:
                chose_icon_pos = resource_icon_pos[1]
                self.set_text(insert="Search wood")
                resource_type = 'wood'

            elif resourse_code == Resource.STONE.value:
                chose_icon_pos = resource_icon_pos[2]
                self.set_text(insert="Search stone")
                resource_type = 'stone'

            elif resourse_code == Resource.GOLD.value:
                chose_icon_pos = resource_icon_pos[3]
                self.set_text(insert="Search gold")
                resource_type = 'gold'


            self.tap(60, 540, 1)
            self.tap(chose_icon_pos[0], chose_icon_pos[1], 1)
            search_pos = self.gui.has_image(ImagePathAndProps.RESOURCE_SEARCH_BUTTON_IMAGE_PATH.value)['result']
            dec_pos = self.gui.has_image(ImagePathAndProps.DECREASING_BUTTON_IMAGE_PATH.value)['result']
            inc_pos = self.gui.has_image(ImagePathAndProps.INCREASING_BUTTON_IMAGE_PATH.value)['result']
            self.tap(inc_pos[0] - 33, inc_pos[1], 0.3)

            repeat_count = 0
            while True:

                # open search resource
                if len(last_resource_pos) > 0:
                    self.back_to_map_gui()
                    self.tap(60, 540, 1)
                    self.tap(chose_icon_pos[0], chose_icon_pos[1], 1)

                # decreasing level
                if should_decreasing_lv:
                    self.set_text(insert="Decreasing search level by 1")
                    self.tap(dec_pos[0], dec_pos[1], 0.3)

                while True:
                    self.tap(search_pos[0], search_pos[1], 2)
                    result = self.gui.has_image(ImagePathAndProps.RESOURCE_SEARCH_BUTTON_IMAGE_PATH.value)
                    if (result is None):
                        break
                    self.set_text(insert="Not found in current Level, decreasing search level by 1")
                    self.tap(dec_pos[0], dec_pos[1], 0.3)

                self.set_text(insert="Resource found")
                self.tap(640, 320, 0.5)

                # check is same pos
                new_resource_pos = self.gui.resource_location_image_to_string()
                if new_resource_pos in last_resource_pos:
                    should_decreasing_lv = True
                    repeat_count = repeat_count + 1
                    self.set_text(insert="Resource point is already in match")
                    if repeat_count > 4:
                        self.set_text(insert="stuck! end task")
                        break
                    else:
                        continue
                last_resource_pos.append(new_resource_pos)
                should_decreasing_lv = False
                gather_button_pos = self.gui.has_image(ImagePathAndProps.RESOURCE_GATHER_BUTTON_IMAGE_PATH.value)[
                    'result']
                self.tap(gather_button_pos[0], gather_button_pos[1], 2)
                result = self.gui.has_image(ImagePathAndProps.NEW_TROOPS_BUTTON_IMAGE_PATH.value)
                if result is None:
                    self.set_text(insert="Not more space for march")
                    return next_task
                new_troops_button_pos = result['result']
                self.tap(new_troops_button_pos[0], new_troops_button_pos[1], 2)
                if not self.config.gatherResourceNoSecondaryCommander:
                    self.set_text(insert="Remove secondary commander")
                    self.tap(473, 501, 0.5)
                match_button_pos = self.gui.has_image(ImagePathAndProps.TROOPS_MATCH_BUTTON_IMAGE_PATH.value)['result']
                self.set_text(insert="March")
                self.tap(match_button_pos[0], match_button_pos[1], 2)
                repeat_count = 0
                self.swipe(300, 360, 400, 360, 1)

        except Exception as e:
            return TaskName.GATHER
        return next_task

    def get_min_resource(self):
        self.tap(725, 20, 1)
        result = self.gui.resource_amount_image_to_string()
        self.set_text(insert="\nFood: {}\nWood: {}\nStone: {}\nGold: {}\n".format(result[0], result[1], result[2], result[3]))
        min = 0
        for i in range(len(result)):
            if result[min] > result[i]:
                min = i
        return min

    # Home
    def back_to_home_gui(self):
        loop_count = 0
        gui_name = None
        while True:
            result = self.get_curr_gui_name();
            gui_name, info = ['UNKNOW', None] if result is None else result
            if gui_name == GuiName.HOME.name:
                break
            elif gui_name == GuiName.MAP.name:
                x_pos, y_pos = info
                self.tap(x_pos, y_pos)
            elif gui_name == GuiName.WINDOW.name:
                self.back(1);
            else:
                self.back(1);
            loop_count = loop_count + 1
            time.sleep(0.5)
        return loop_count

    def find_home(self):
        result = self.gui.has_image(ImagePathAndProps.GREEN_HOME_BUTTON_IMG_PATH.value)
        if result is None:
            return None
        info = result['result']
        x_pos, y_pos = info[0], info[1]
        self.tap(x_pos, y_pos, 2)

    def home_gui_full_view(self):
        self.tap(60, 540, 0.5)
        self.tap(1105, 200, 1)
        self.tap(1220, 35, 2)

        # self.swipe(300, 360, 980, 360, 5)
        # self.find_home()

    # Building Position
    def find_building_title(self):
        result = self.gui.has_image(ImagePathAndProps.BUILDING_TITLE_MARK_IMG_PATH.value)
        if result is None:
            return None
        x0, y0, x1, y1 = aircv_rectangle_to_box(result["rectangle"])
        return x0, y0, x1, y1

    # Menu
    def menu_should_open(self, shouldOpen=False):
        # close menu if open
        path, size, box, threshold, least_diff, gui = ImagePathAndProps.MENU_BUTTON_IMAGE_PATH.value
        x0, y0, x1, y1 = box
        c_x, c_y = x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2
        open, _, _ = self.gui.check(ImagePathAndProps.MENU_OPENED_IMAGE_PATH.value);
        if shouldOpen and not open:
            self.tap(c_x, c_y, 0.5)
        elif not shouldOpen and open:
            self.tap(c_x, c_y, 0.5)

    # Map
    def back_to_map_gui(self):
        loop_count = 0
        gui_name = None
        while True:
            result = self.get_curr_gui_name();
            gui_name, pos = ['UNKNOW', None] if result is None else result
            if gui_name == GuiName.MAP.name:
                break
            elif gui_name == GuiName.HOME.name:
                x_pos, y_pos = pos
                self.tap(x_pos, y_pos)
            elif gui_name == GuiName.WINDOW.name:
                self.back(1);
            else:
                self.back(1);
            loop_count = loop_count + 1
            time.sleep(0.5)
        return loop_count

    def get_curr_gui_name(self):
        if not self.isRoKRunning():
            self.set_text(insert='game is not running, try to start game')
            self.runOfRoK()
            start = time.time()
            end = start
            while end - start <= 300 and self.isRoKRunning():
                result = self.gui.get_curr_gui_name()
                if result is None:
                    time.sleep(5)
                    end = time.time()
                else:
                    break

        pos_list = None
        while True:
            result = self.gui.get_curr_gui_name()
            gui_name, pos = ['UNKNOW', None] if result is None else result
            if gui_name == GuiName.VERIFICATION_VERIFY.name:
                self.tap(pos[0], pos[1], 5)
            elif gui_name == GuiName.VERIFICATION_CLOSE_REFRESH_OK.name and pos_list is None:
                pos_list = self.pass_verification()
            else:
                return result

    def pass_verification(self):
        self.set_text(insert='pass verification')
        box = (400, 0, 880, 720)
        ok = [780, 680]
        img = self.gui.get_curr_device_screen_img()
        img = img.crop(box)
        pos_list = haoi.solve_verification(self.config.haoiUser, self.config.haoiRebate, img)
        if pos_list is None:
            self.set_text(insert='fail to pass verification')
            return None

        for pos in pos_list:
            self.tap(400 + pos[0], pos[1], 1)
        self.tap(780, 680, 5)
        return pos_list

    # Action
    def back(self, sleep_time=0.5):
        cmd = 'input keyevent 4'
        self.device.shell(cmd)
        time.sleep(sleep_time)

    # duration is in milliseconds
    def swipe(self, x_f, y_f, x_t, y_t, times=1, duration=300):
        cmd = "input swipe {} {} {} {} {}".format(x_f, y_f, x_t, y_t, duration)
        for i in range(times):
            self.device.shell(cmd)
            time.sleep(duration / 1000 + 0.2)

    # long_press_duration is in milliseconds
    def tap(self, x, y, sleep_time=0.1, long_press_duration=-1):
        cmd = None
        if long_press_duration > -1:
            cmd = 'input swipe {} {} {} {} {}'.format(x, y, x, y, long_press_duration)
            sleep_time = long_press_duration / 1000 + 0.2
        else:
            cmd = 'input tap {} {}'.format(x, y)

        str = self.device.shell(cmd)
        time.sleep(sleep_time)

    def isRoKRunning(self):
        cmd = ('dumpsys activity activities')
        str = self.device.shell(cmd)
        return str.find('com.lilithgame.roc.gp') != -1

    def runOfRoK(self):
        cmd = 'am start -n com.lilithgame.roc.gp/com.harry.engine.MainActivity'
        str = self.device.shell(cmd)

    def set_text(self, **kwargs):
        dt_string = datetime.now().strftime("[%H:%M:%S]")
        title = 'title'
        text_list = 'text_list'
        insert = 'insert'
        remove = 'remove'
        replace = 'replace'
        index = 'index'

        if title in kwargs:
            self.text[title] = kwargs[title]

        if replace in kwargs:
            self.text[text_list][kwargs[index]] = dt_string + " " + kwargs[replace].lower()

        if insert in kwargs:
            self.text[text_list].insert(kwargs.get('index', 0), dt_string + " "+ kwargs[insert].lower())

        if remove in kwargs and kwargs.get(remove, False):
            self.text[text_list].clear()

        self.text_update_event(self.text)


class BotConfig:
    def __init__(self, config={}):
        self.enableBreak = config.get('enableBreak', True)
        self.breakTime = config.get('breakTime', 60 * 3)

        # Collecting
        self.enableCollecting = config.get('enableCollecting', True)

        # Producing
        self.enableMaterialProduce = config.get('enableMaterialProduce', True)

        # Tavern
        self.enableTavern = config.get('enableTavern', True)

        # Training
        self.enableTraining = config.get('enableTraining', True)

        self.action_wait_time = config.get('action_wait_time', 1)
        self.hasBuildingPos = config.get('hasBuildingPos', False)
        self.gatherResourceNoSecondaryCommander = config.get('gatherResourceNoSecondaryCommander', True)

        self.trainBarracksTrainingLevel = config.get('trainBarracksTrainingLevel',
                                                     TrainingAndUpgradeLevel.T1.value)
        self.trainBarracksUpgradeLevel = config.get('trainBarracksUpgradeLevel',
                                                    TrainingAndUpgradeLevel.T1.value)

        self.trainArcheryRangeTrainingLevel = config.get('trainArcheryRangeTrainingLevel',
                                                         TrainingAndUpgradeLevel.T1.value)
        self.trainArcheryRangeUpgradeLevel = config.get('trainArcheryRangeUpgradeLevel',
                                                        TrainingAndUpgradeLevel.T1.value)

        self.trainStableTrainingLevel = config.get('trainStableTrainingLevel',
                                                   TrainingAndUpgradeLevel.T1.value)
        self.trainStableUpgradeLevel = config.get('trainArcheryRangeUpgradeLevel',
                                                  TrainingAndUpgradeLevel.T1.value)

        self.trainSiegeWorkshopTrainingLevel = config.get('trainSiegeWorkshopTrainingLevel',
                                                          TrainingAndUpgradeLevel.T1.value)
        self.trainSiegeWorkshopUpgradeLevel = config.get('trainSiegeWorkshopUpgradeLevel',
                                                         TrainingAndUpgradeLevel.T1.value)

        # Quest
        self.claimQuests = config.get('claimQuests', True)

        # Alliance
        self.allianceAction = config.get('allianceAction', True)

        # Gather resource
        self.gatherResource = config.get('gatherResource', True)

        self.haoiUser = config.get('haoiUser', None)
        self.haoiRebate = config.get('haoiRebate', None)
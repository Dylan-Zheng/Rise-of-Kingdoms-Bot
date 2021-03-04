from bot_related.device_gui_detector import GuiName, GuiDetector
from bot_related.bot_config import TrainingAndUpgradeLevel, BotConfig
from bot_related import haoi, twocaptcha
from config import HAO_I, TWO_CAPTCHA
from filepath.file_relative_paths import ImagePathAndProps, BuffsImageAndProps, ItemsImageAndProps
from datetime import datetime
from utils import aircv_rectangle_to_box
from enum import Enum
from filepath.constants import RESOURCES, SPEEDUPS, BOOSTS, EQUIPMENT, OTHER, MAP, HOME

import config
import traceback
import math
import time

DEFAULT_RESOLUTION = {'height': 720, 'width': 1280}

verification_method = None


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
        self.config_update_event = lambda **kw: kw

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
            curr_task = TaskName.INIT_BUILDING_POS

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

            # init building position if need
            if not self.config.hasBuildingPos or curr_task == TaskName.INIT_BUILDING_POS:
                curr_task = self.init_building_pos()

            # collecting resource
            if curr_task == TaskName.COLLECTING and self.config.enableCollecting:
                curr_task = self.collecting_soldiers_resources_and_help(TaskName.VIP_CHEST)
            elif curr_task == TaskName.COLLECTING:
                curr_task = TaskName.VIP_CHEST

            if curr_task == TaskName.VIP_CHEST and self.config.enableVipClaimChest:
                curr_task = self.claim_vip(TaskName.CLAIM_QUEST)
            elif curr_task == TaskName.VIP_CHEST:
                curr_task = TaskName.CLAIM_QUEST

            # claim quests
            if curr_task == TaskName.CLAIM_QUEST and self.config.claimQuests:
                curr_task = self.claim_quests(TaskName.ALLIANCE)
            elif curr_task == TaskName.CLAIM_QUEST:
                curr_task = TaskName.ALLIANCE

            # alliance
            if curr_task == TaskName.ALLIANCE and self.config.allianceAction:
                curr_task = self.alliance(TaskName.METARIALS)
            elif curr_task == TaskName.ALLIANCE:
                curr_task = TaskName.METARIALS

            # material
            if curr_task == TaskName.METARIALS and self.config.enableMaterialProduce:
                curr_task = self.materials(TaskName.TAVERN)
            elif curr_task == TaskName.METARIALS:
                curr_task = TaskName.TAVERN

            # tavern
            if curr_task == TaskName.TAVERN and self.config.enableTavern:
                curr_task = self.tavern(TaskName.TRAINING)
            elif curr_task == TaskName.TAVERN:
                curr_task = TaskName.TRAINING

            # train soldiers
            if curr_task == TaskName.TRAINING and self.config.enableTraining:
                curr_task = self.training_and_upgrade(TaskName.BARBARIANS)
            elif curr_task == TaskName.TRAINING:
                curr_task = TaskName.BARBARIANS

            # Attack Barbarians
            if curr_task == TaskName.BARBARIANS and self.config.attackBarbarians:
                curr_task = self.attack_barbarians(next_task=TaskName.GATHER)
            elif curr_task == TaskName.BARBARIANS:
                curr_task = TaskName.GATHER

            # gather resource
            if curr_task == TaskName.GATHER and self.config.gatherResource:
                curr_task = self.gather_resource(TaskName.BREAK)
            elif curr_task == TaskName.GATHER:
                curr_task = TaskName.BREAK

        return

    # screen range x0 250, x1 950, y0 95, y1 615
    def init_building_pos(self, next_task=TaskName.COLLECTING):

        try:
            self.set_text(title='Init Building Position', remove=True)
            self.set_text(insert='progress: 0%', index=0)
            self.set_text(append='init view')

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
                    self.set_text(insert='tap at ({}, {})'.format(x, y), index=1)
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
                            self.set_text(insert='<{}> on position ({}, {})'.format(name, x, y), index=1)
                            self.back()

                    self.tap(x_start, y_start)
                    self.set_text(
                        replace='progress: {}%'.format(int(((row * x_times) + (col + 1)) / total * 100)),
                        index=0)

                    # bot_print("{}/{}".format((row * x_times) + (col + 1), total))

            # save building pos to json
            self.config.hasBuildingPos = True
            self.building_pos_update_event(building_pos=self.building_pos, prefix=self.device.serial.replace(':', "_"))
            self.config_update_event(config=self.config, prefix=self.device.serial.replace(':', "_"))
        except Exception as e:
            traceback.print_exc()
            self.config.hasBuildingPos = False
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
                self.set_text(insert='tap {} at position ({},{})'.format(name, x, y))
                self.tap(x, y)
                self.tap(x_e, y_e)

        except Exception as e:
            traceback.print_exc()
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
            for i in range(20):
                result = self.gui.has_image(ImagePathAndProps.QUEST_CLAIM_BUTTON_IMAGE_PATH.value)
                if result is None:
                    break
                x, y = result["result"]
                self.set_text(insert='Tap claim button at ({}, {})'.format(x, y))
                self.tap(x, y, 0.5)

            self.set_text(insert='Claim Daily Objective')
            self.tap(daily_objectives_tap_pos[0], daily_objectives_tap_pos[1], 1)
            for i in range(20):
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
            traceback.print_exc()
            return TaskName.CLAIM_QUEST
        return next_task

    def claim_vip(self, next_task=TaskName.CLAIM_QUEST):
        vip_pos = (150, 65)
        vip_point_chest = (1010, 180)
        vip_free_chest = (920, 400)
        self.set_text(title='Claim VIP Chest', remove=True)
        self.back_to_home_gui()
        # tap on vip
        self.set_text(insert='Open VIP')
        x, y = vip_pos
        self.tap(x, y, 2)
        # tap on vip point chest
        self.set_text(insert='Claim daily vip point')
        x, y = vip_point_chest
        self.tap(x, y, 1)
        # tap on free chest
        self.set_text(insert='Claim daily free vip chest')
        x, y = vip_free_chest
        self.tap(x, y, 1)
        return next_task

    def alliance(self, next_task=TaskName.METARIALS):
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
                    treasure = (330, 410)
                    x, y = gifts_pos
                    self.tap(x, y, 2)

                    # collecting rate gifts
                    self.set_text(insert='Claim rate gift')
                    x, y = rate_pos
                    self.tap(x, y, 1)
                    for i in range(20):
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

                    # collecting treasure of white crystal
                    x, y = treasure
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
            traceback.print_exc()
            return TaskName.ALLIANCE
        return next_task

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
        for i in range(20):
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
                        self.set_text(insert='Upgrade T{}({})'.format(i + 1, config[4]))
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
            traceback.print_exc()
            return TaskName.TRAINING
        return next_task

    def set_barbarians_level(self, level):
        max_pos = (375, 405)
        min_pos = (168, 405)

        dec_pos = self.gui.has_image(ImagePathAndProps.DECREASING_BUTTON_IMAGE_PATH.value)['result']
        inc_pos = self.gui.has_image(ImagePathAndProps.INCREASING_BUTTON_IMAGE_PATH.value)['result']

        # set to max level
        x, y = max_pos
        self.tap(x, y)
        # try to get max lv. in integer
        max_lv = self.gui.barbarians_level_image_to_string()
        self.set_text(insert="Max level is {}".format(max_lv))
        if max_lv != -1:
            x = max_pos[0] if level > max_pos[0] or level >= 99 else (level / max_lv) * (max_pos[0] - min_pos[0]) + min_pos[0]
            y = max_pos[1]
            self.tap(x, y)
            curr_lv = self.gui.barbarians_level_image_to_string()
            if curr_lv == -1:
                self.set_text(insert="Fail to read current level, set to lv.1".format(curr_lv))
            else:
                self.set_text(insert="current level is {}".format(curr_lv))
            btn_pos = inc_pos if curr_lv < level else dec_pos
            for i in range(int(abs(level - curr_lv))):
                x, y = btn_pos
                self.tap(x, y)

    def attack_barbarians(self, next_task=TaskName.GATHER):
        icon_pos = (255, 640)
        center_pos = (640, 320)


        self.set_text(title='Attack Barbarians', remove=True)
        self.set_text(insert="Search barbarians")
        self.back_to_map_gui()

        # tap on magnifier
        self.tap(60, 540, 1)
        # tap on barbarians icon
        x, y = icon_pos
        self.tap(x, y, 1)

        # set barbarians level
        self.set_barbarians_level(self.config.barbariansLevel)

        # tap search button
        search_pos = self.gui.has_image(ImagePathAndProps.RESOURCE_SEARCH_BUTTON_IMAGE_PATH.value)['result']
        x, y = search_pos
        self.tap(x, y, 2)
        x, y = center_pos
        self.tap(x, y, 1)

        return next_task

    def gather_resource(self, next_task=TaskName.BREAK):
        self.set_text(title='Gather Resource', remove=True)

        if self.config.useGatheringBoosts:
            b_buff_props = BuffsImageAndProps.ENHANCED_GATHER_BLUE.value
            p_buff_props = BuffsImageAndProps.ENHANCED_GATHER_PURPLE.value
            b_item_props = ItemsImageAndProps.ENHANCED_GATHER_BLUE.value
            p_item_props = ItemsImageAndProps.ENHANCED_GATHER_PURPLE.value
            has_blue = self.has_buff(MAP, b_buff_props)
            has_purple = self.has_buff(MAP, p_buff_props)
            if not has_blue and not has_purple:
                self.set_text(insert='use gathering boosts')
                self.use_item(MAP, [b_item_props, p_item_props])
            else:
                self.set_text(insert="gathering boosts buff is already on")

        last_resource_pos = []
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

            elif resourse_code == Resource.WOOD.value:
                chose_icon_pos = resource_icon_pos[1]
                self.set_text(insert="Search wood")

            elif resourse_code == Resource.STONE.value:
                chose_icon_pos = resource_icon_pos[2]
                self.set_text(insert="Search stone")

            elif resourse_code == Resource.GOLD.value:
                chose_icon_pos = resource_icon_pos[3]
                self.set_text(insert="Search gold")

            # tap on magnifier
            self.tap(60, 540, 1)
            self.tap(chose_icon_pos[0], chose_icon_pos[1], 1)
            search_pos = self.gui.has_image(ImagePathAndProps.RESOURCE_SEARCH_BUTTON_IMAGE_PATH.value)['result']
            dec_pos = self.gui.has_image(ImagePathAndProps.DECREASING_BUTTON_IMAGE_PATH.value)['result']
            inc_pos = self.gui.has_image(ImagePathAndProps.INCREASING_BUTTON_IMAGE_PATH.value)['result']
            self.tap(inc_pos[0] - 33, inc_pos[1], 0.3)

            repeat_count = 0
            for i in range(10):

                # open search resource
                if len(last_resource_pos) > 0:
                    self.back_to_map_gui()
                    self.tap(60, 540, 1)
                    self.tap(chose_icon_pos[0], chose_icon_pos[1], 1)

                # decreasing level
                if should_decreasing_lv:
                    self.set_text(insert="Decreasing level by 1")
                    self.tap(dec_pos[0], dec_pos[1], 0.3)

                for j in range(5):
                    self.tap(search_pos[0], search_pos[1], 2)
                    result = self.gui.has_image(ImagePathAndProps.RESOURCE_SEARCH_BUTTON_IMAGE_PATH.value)
                    if result is None:
                        break
                    self.set_text(insert="Not found, decreasing level by 1 [{}]".format(j))
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
                if self.config.gatherResourceNoSecondaryCommander:
                    self.set_text(insert="Remove secondary commander")
                    self.tap(473, 501, 0.5)
                match_button_pos = self.gui.has_image(ImagePathAndProps.TROOPS_MATCH_BUTTON_IMAGE_PATH.value)['result']
                self.set_text(insert="March")
                self.tap(match_button_pos[0], match_button_pos[1], 2)
                repeat_count = 0
                self.swipe(300, 720, 400, 360, 1)

        except Exception as e:
            traceback.print_exc()
            return TaskName.GATHER
        return next_task

    def get_min_resource(self):
        self.tap(725, 20, 1)
        result = self.gui.resource_amount_image_to_string()
        self.set_text(
            insert="\nFood: {}\nWood: {}\nStone: {}\nGold: {}\n".format(result[0], result[1], result[2], result[3]))

        ratio = [
            self.config.gatherResourceRatioFood,
            self.config.gatherResourceRatioWood,
            self.config.gatherResourceRatioStone,
            self.config.gatherResourceRatioGold
        ]

        ras = sum(ratio)
        res = sum(result)

        diff = []
        for i in range(4):
            diff.append((ratio[i] / ras) - ((result[i] if result[i] > -1 else 0) / res))

        m = 0
        for i in range(len(result)):
            if diff[m] < diff[i]:
                m = i
        return m

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

    # Building Position
    def find_building_title(self):
        result = self.gui.has_image(ImagePathAndProps.BUILDING_TITLE_MARK_IMG_PATH.value)
        if result is None:
            return None
        x0, y0, x1, y1 = aircv_rectangle_to_box(result["rectangle"])
        return x0, y0, x1, y1

    # Menu
    def menu_should_open(self, should_open=False):
        # close menu if open
        path, size, box, threshold, least_diff, gui = ImagePathAndProps.MENU_BUTTON_IMAGE_PATH.value
        x0, y0, x1, y1 = box
        c_x, c_y = x0 + (x1 - x0) / 2, y0 + (y1 - y0) / 2
        is_open, _, _ = self.gui.check(ImagePathAndProps.MENU_OPENED_IMAGE_PATH.value);
        if should_open and not is_open:
            self.tap(c_x, c_y, 0.5)
        elif not should_open and is_open:
            self.tap(c_x, c_y, 0.5)

    # Map
    def back_to_map_gui(self):
        loop_count = 0
        gui_name = None
        while True:
            result = self.get_curr_gui_name()
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
        try:
            self.set_text(insert='pass verification')
            box = (400, 0, 880, 720)
            ok = [780, 680]
            img = self.gui.get_curr_device_screen_img()
            img = img.crop(box)
            pos_list = None
            if config.global_config.method == HAO_I:
                pos_list = haoi.solve_verification(img)
            elif config.global_config.method == TWO_CAPTCHA:
                pos_list = twocaptcha.solve_verification(img)

            if pos_list is None:
                self.set_text(insert='fail to pass verification')
                return None

            for pos in pos_list:
                self.tap(400 + pos[0], pos[1], 1)
            self.tap(780, 680, 5)

        except Exception as e:
            traceback.print_exc()

        return pos_list

    def has_buff(self, checking_location, buff_img_props):
        # Where to check
        if checking_location == HOME:
            self.back_to_home_gui()
        elif checking_location == MAP:
            self.back_to_map_gui()
        else:
            return False
        # Start Checking
        result = self.gui.has_image(buff_img_props)
        if result is None:
            return False
        return True

    def use_item(self, using_location, item_img_props_list):

        # Where to use the item
        if using_location == HOME:
            self.back_to_home_gui()
        elif using_location == MAP:
            self.back_to_map_gui()
        else:
            return False

        items_icon_pos = (930, 675)
        use_btn_pos = (980, 600)

        for item_img_props in item_img_props_list:
            path, size, box, threshold, least_diff, tab_name = item_img_props

            tabs_pos = {
                RESOURCES: (250, 80),
                SPEEDUPS: (435, 80),
                BOOSTS: (610, 80),
                EQUIPMENT: (790, 80),
                OTHER: (970, 80),
            }
            # open menu
            self.menu_should_open(True)
            # open items window
            x, y = items_icon_pos
            self.tap(x, y, 2)
            # tap on tab
            x, y = tabs_pos[tab_name]
            self.tap(x, y, 1)
            # find item, and tap it
            result = self.gui.has_image(item_img_props)
            if result is None:
                continue
            x, y = result['result']
            self.tap(x, y, 0.5)
            # tap on use Item
            x, y = use_btn_pos
            self.tap(x, y)
            return True
        return False

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
        append = 'append'

        if title in kwargs:
            self.text[title] = kwargs[title]

        if replace in kwargs:
            self.text[text_list][kwargs[index]] = dt_string + " " + kwargs[replace].lower()

        if insert in kwargs:
            self.text[text_list].insert(kwargs.get(index, 0), dt_string + " " + kwargs[insert].lower())

        if append in kwargs:
            self.text[text_list].append(dt_string + " " + kwargs[append].lower())

        if remove in kwargs and kwargs.get(remove, False):
            self.text[text_list].clear()

        self.text_update_event(self.text)

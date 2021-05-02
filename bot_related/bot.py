import threading

from bot_related.bot_config import BotConfig
from bot_related.device_gui_detector import GuiDetector
from tasks.Alliance import Alliance
from tasks.Barbarians import Barbarians
from tasks.Break import Break
from tasks.ClaimQuests import ClaimQuests
from tasks.ClaimVip import ClaimVip
from tasks.Collecting import Collecting
from tasks.GatherResource import GatherResource
from tasks.LocateBuildings import LocateBuilding
from tasks.Materials import Materials
from tasks.Restart import Restart
from tasks.Scout import Scout
from tasks.ScreenShot import ScreenShot
from tasks.Tavern import Tavern
from tasks.Training import Training
from tasks.constants import TaskName
from utils import stop_thread

DEFAULT_RESOLUTION = {'height': 720, 'width': 1280}


class Bot:

    def __init__(self, device, config={}):
        self.curr_thread = None
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

        # tasks
        self.restart_task = Restart(self)
        self.break_task = Break(self)
        self.alliance_task = Alliance(self)
        self.barbarians_task = Barbarians(self)
        self.claim_quests_task = ClaimQuests(self)
        self.claim_vip_task = ClaimVip(self)
        self.collecting_task = Collecting(self)
        self.gather_resource_task = GatherResource(self)
        self.locate_building_task = LocateBuilding(self)
        self.materials_task = Materials(self)
        self.scout_task = Scout(self)
        self.tavern_task = Tavern(self)
        self.training = Training(self)

        # Other task
        self.screen_shot_task = ScreenShot(self)

    def start(self, fn):
        self.curr_thread = threading.Thread(target=fn)
        self.curr_thread.start()
        return self.curr_thread

    def stop(self):
        if self.curr_thread is not None:
            stop_thread(self.curr_thread)
            self.curr_thread = None
            return True
        return False

    def get_city_image(self):
        return self.screen_shot_task.do_city_screen()

    def do_task(self, curr_task=TaskName.COLLECTING):

        round_count = 0

        if self.building_pos is None:
            curr_task = TaskName.INIT_BUILDING_POS

        while True:

            # restart
            if curr_task == TaskName.KILL_GAME and self.config.enableStop \
                    and round_count % self.config.stopDoRound == 0:
                curr_task = self.restart_task.do(TaskName.BREAK)
            elif curr_task == TaskName.KILL_GAME:
                curr_task = TaskName.BREAK

            # init building position if need
            if not self.config.hasBuildingPos or curr_task == TaskName.INIT_BUILDING_POS:
                curr_task = self.locate_building_task.do(next_task=TaskName.COLLECTING)

            # break
            if curr_task == TaskName.BREAK and self.config.enableBreak:
                curr_task = self.break_task.do(TaskName.COLLECTING)
            elif curr_task == TaskName.BREAK:
                curr_task = self.break_task.do_no_wait(TaskName.COLLECTING)

            # collecting resource
            if curr_task == TaskName.COLLECTING and self.config.enableCollecting:
                curr_task = self.collecting_task.do(TaskName.VIP_CHEST)
            elif curr_task == TaskName.COLLECTING:
                curr_task = TaskName.VIP_CHEST

            # claim vip chest
            if curr_task == TaskName.VIP_CHEST and self.config.enableVipClaimChest \
                    and round_count % self.config.vipDoRound == 0:
                curr_task = self.claim_vip_task.do(TaskName.CLAIM_QUEST)
            elif curr_task == TaskName.VIP_CHEST:
                curr_task = TaskName.CLAIM_QUEST

            # claim quests
            if curr_task == TaskName.CLAIM_QUEST and self.config.claimQuests \
                    and round_count % self.config.questDoRound == 0:
                curr_task = self.claim_quests_task.do(TaskName.ALLIANCE)
            elif curr_task == TaskName.CLAIM_QUEST:
                curr_task = TaskName.ALLIANCE

            # alliance
            if curr_task == TaskName.ALLIANCE and self.config.allianceAction \
                    and round_count % self.config.allianceDoRound == 0:
                curr_task = self.alliance_task.do(TaskName.METARIALS)
            elif curr_task == TaskName.ALLIANCE:
                curr_task = TaskName.METARIALS

            # material
            if curr_task == TaskName.METARIALS and self.config.enableMaterialProduce \
                    and round_count % self.config.materialDoRound == 0:
                curr_task = self.materials_task.do(TaskName.TAVERN)
            elif curr_task == TaskName.METARIALS:
                curr_task = TaskName.TAVERN

            # tavern
            if curr_task == TaskName.TAVERN and self.config.enableTavern:
                curr_task = self.tavern_task.do(TaskName.TRAINING)
            elif curr_task == TaskName.TAVERN:
                curr_task = TaskName.TRAINING

            # train soldiers
            if curr_task == TaskName.TRAINING and self.config.enableTraining:
                curr_task = self.training.do(TaskName.BARBARIANS)
            elif curr_task == TaskName.TRAINING:
                curr_task = TaskName.BARBARIANS

            # Attack Barbarians
            if curr_task == TaskName.BARBARIANS and self.config.attackBarbarians:
                curr_task = self.barbarians_task.do(next_task=TaskName.GATHER)
            elif curr_task == TaskName.BARBARIANS:
                curr_task = TaskName.GATHER

            # gather resource
            if curr_task == TaskName.GATHER and self.config.gatherResource:
                curr_task = self.gather_resource_task.do(TaskName.SCOUT)
            elif curr_task == TaskName.GATHER:
                curr_task = TaskName.SCOUT

            # scout
            if curr_task == TaskName.SCOUT and self.config.enableScout:
                curr_task = self.scout_task.do(TaskName.BREAK)
            elif curr_task == TaskName.SCOUT:
                curr_task = TaskName.BREAK

            round_count = round_count + 1
        return

    
    def isRoKRunning(self):
        cmd = 'dumpsys window windows | grep mCurrentFocus'
        str = self.device.shell(cmd)
        return str.find('com.lilithgame.roc.gp/com.harry.engine.MainActivity') != -1


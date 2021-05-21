from tkinter import Tk, N, W
from tkinter.ttk import Notebook, Frame
from gui.setting_frame import SettingFrame
from gui.bottom_frame import BottomFrame
from gui.device_list_frame import DeviceListFrame
from config import load_config
from bot_related import twocaptcha, haoi
import adb
from version import version
import config


class MainWindow:

    def __init__(self):
        self.adb = adb.bridge
        config.global_config = load_config()
        twocaptcha.key = config.global_config.twocaptchaKey
        haoi.userstr = config.global_config.haoiUser
        haoi.rebate = config.global_config.haoiRebate

        self.window = Tk()
        self.size = config.global_config.screenSize

        self.window.title('Rise Of Kingdom Bot ({})'.format(version))
        self.window.geometry('{}x{}'.format(self.size[0], self.size[1]))
        self.window.resizable(0, 0)

        self.curr_frame = None
        self.last_frame = None
        self.setting_frame = None

        self.notebook = Notebook(self.window, height=self.size[1] - 80)

        main_frame = Frame(self.notebook, width=self.size[0], height=self.size[1])

        dlf = DeviceListFrame(self.notebook, main_frame, width=self.size[0], height=self.size[1])

        sf = SettingFrame(self.notebook, width=self.size[0], height=self.size[1])
        self.setting_frame = sf
        sf.grid(row=0, column=0, sticky=N + W)
        sf.grid_propagate(False)

        self.notebook.add(dlf, text='Device List')
        self.notebook.add(main_frame, text='Display Device')
        self.notebook.add(sf, text='Setting')
        self.notebook.grid(row=0, column=0, sticky=N + W, pady=(10, 0))

        bf = BottomFrame(self.window, width=self.size[0], height=self.size[1])
        bf.grid(row=1, column=0, sticky=N + W, padx=10, pady=(10, 0))

    def run(self):
        self.window.mainloop()

from tkinter import Tk, N, W
from tkinter.ttk import Notebook
from gui.setting_frame import SettingFrame
from gui.bottom_frame import BottomFrame
from gui.selected_device_frame import SelectedDeviceFrame
from config import load_config
from bot_related import twocaptcha, haoi

import config


class MainWindow:

    def __init__(self, adb, size=(450, 850)):
        self.adb = adb
        config.global_config = load_config()
        twocaptcha.key = config.global_config.twocaptchaKey
        haoi.userstr = config.global_config.haoiUser
        haoi.rebate = config.global_config.haoiRebate

        self.window = Tk()
        self.size = size

        self.window.title('Rise Of Kingdom Bot')
        self.window.geometry('{}x{}'.format(size[0], size[1]))
        self.window.resizable(0, 0)

        self.curr_frame = None
        self.last_frame = None
        self.main_frame_list = []
        self.setting_frame = None

        tab = Notebook(self.window, height=size[1] - 80)

        device = self.adb.get_device()
        mf = SelectedDeviceFrame(self.window, self.adb.get_device(), width=size[0], height=size[1])
        self.curr_frame = mf
        self.main_frame_list.append(mf)
        mf.grid(row=0, column=0, sticky=N + W)
        mf.grid_propagate(False)

        sf = SettingFrame(self.window, width=size[0], height=size[1])
        self.setting_frame = sf
        sf.grid(row=0, column=0, sticky=N + W)
        sf.grid_propagate(False)

        tab.add(mf, text=mf.device.serial)
        tab.add(sf, text='Setting')
        tab.grid(row=0, column=0, sticky=N + W, pady=(10, 0))

        bf = BottomFrame(self.window, width=size[0], height=size[1])
        bf.grid(row=1, column=0, sticky=N + W, padx=10, pady=(10, 0))

    def run(self):
        self.window.mainloop()

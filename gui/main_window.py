from tkinter import Tk, N, W
from gui.top_frame import TopFrame, SettingFrame
from gui.main_frame import MainFrame

from config import load_config

from bot_related import twocaptcha
from bot_related import haoi

import config

import json





class MainWindow:

    def __init__(self, adb, size=(450, 800)):
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

        tf = TopFrame(self.window, width=size[0], height=size[1])
        tf.buttons_setup(on_setting_click=self.on_setting_click)
        tf.grid(row=0, column=0, sticky=N + W, padx=10, pady=(10, 0))

        mf = MainFrame(self.window, self.adb.get_device(), width=size[0], height=size[1])
        self.curr_frame = mf
        self.main_frame_list.append(mf)
        mf.grid(row=1, column=0, sticky=N + W)
        mf.grid_propagate(False)

        sf = SettingFrame(self.window, width=size[0], height=size[1])
        self.setting_frame = sf
        sf.grid(row=1, column=0, sticky=N + W)
        sf.grid_propagate(False)
        sf.grid_forget()

    def run(self):
        self.window.mainloop()

    def on_setting_click(self, btn):
        if self.curr_frame == self.setting_frame:
            self.setting_frame.grid_forget()
            self.last_frame.grid()

            self.curr_frame = self.last_frame
            self.last_frame = self.setting_frame
            btn.config(text='Setting')
        else:
            self.setting_frame.grid()
            self.curr_frame.grid_forget()

            self.last_frame = self.curr_frame
            self.curr_frame = self.setting_frame
            btn.config(text='Back')




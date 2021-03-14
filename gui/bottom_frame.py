from tkinter import Frame, Label, N, W
import webbrowser
from utils import get_last_version_number
from version import version
import threading

url = "https://github.com/Dylan-Zheng/Rise-of-Kingdoms-Bot"


class BottomFrame(Frame):

    def __init__(self, windows, cnf={}, **kwargs):
        Frame.__init__(self, windows, kwargs)
        self.windows_size = [kwargs['width'], kwargs['height']]

        label = Label(self, text="Welcome to use Rise of Kingdoms Bot, You see update on")

        def callback():
            last_version = get_last_version_number()
            if last_version != version:
                label.config(text='There is new version {}, download at'.format(last_version))

        threading.Thread(target=callback).start()

        link = Label(self, text="GitHub", fg="blue", cursor="hand2")
        link.bind("<Button-1>", lambda e: webbrowser.open_new(url))

        label.grid(row=0, column=0, sticky=N + W)
        link.grid(row=0, column=1, sticky=N + W)

from tkinter import Frame, Label, N, W
import webbrowser
from utils import get_last_info
from version import version
import threading

url = "https://github.com/Dylan-Zheng/Rise-of-Kingdoms-Bot"


class BottomFrame(Frame):

    def __init__(self, windows, cnf={}, **kwargs):
        Frame.__init__(self, windows, kwargs)
        self.windows_size = [kwargs['width'], kwargs['height']]

        label = Label(self, text="Welcome to use Rise of Kingdoms Bot, see update on")
        link = Label(self, text="GitHub", fg="blue", cursor="hand2")

        def callback():

            info = get_last_info()
            if info.get('version', version) > version:
                label.config(text='There is new version {}, download at'.format(info['version']))
                return

            if info.get('shouldUpdateInfo', False):

                label_info = info.get('label', {'update': False})
                if label_info['update']:
                    label.config(text=label_info['text'])
                    label.grid(row=label_info['row'], column=label_info['column'])
                else:
                    label.grid_forget()

                link_info = info.get('link', {'update': False})
                if label_info['update']:
                    link.config(text=link_info['text'])
                    link.bind("<Button-1>", lambda e: webbrowser.open_new(info.get('url', url)))
                    link.grid(row=link_info['row'], column=link_info['column'])
                else:
                    link.grid_forget()

        threading.Thread(target=callback).start()

        link.bind("<Button-1>", lambda e: webbrowser.open_new(url))
        label.grid(row=0, column=0, sticky=N + W)
        link.grid(row=0, column=1, sticky=N + W)

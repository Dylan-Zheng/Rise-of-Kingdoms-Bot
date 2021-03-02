from tkinter import Frame, Label, N, W
import webbrowser

url = "https://github.com/Dylan-Zheng/Rise-of-Kingdoms-Bot"


class BottomFrame(Frame):

    def __init__(self, windows, cnf={}, **kwargs):
        Frame.__init__(self, windows, kwargs)
        self.windows_size = [kwargs['width'], kwargs['height']]

        label = Label(self, text="Welcome to use Rise of Kingdoms Bot, You can check update on")

        link = Label(self, text="GitHub", fg="blue", cursor="hand2")
        link.bind("<Button-1>", lambda e: webbrowser.open_new(url))

        label.grid(row=0, column=0, sticky = N + W)
        link.grid(row=0, column=1, sticky = N + W)


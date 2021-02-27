from gui.creator import load_bot_config
from gui.creator import load_building_pos
from gui.creator import write_building_pos
from gui.creator import button

from tkinter import Label, Frame, Text
from tkinter import N, W, END, INSERT, LEFT

from utils import stop_thread
from gui import all_title_fns as atf
from bot_related.bot import Bot

import threading


verification_method = None

class MainFrame(Frame):

    def __init__(self, windows, device, cnf={}, **kwargs):
        Frame.__init__(self, windows, kwargs)

        self.bot = None
        self.device = device
        self.bot_config = load_bot_config(device.serial.replace(':', "_"))
        self.bot_building_pos = load_building_pos(device.serial.replace(':', "_"))
        self.bot_thread = None
        self.windows_size = [kwargs['width'], kwargs['height']]

        display_frame, self.task_title, self.task_text = self.task_display_frame()
        config_frame = self.config_frame()
        bottom_frame = self.bottom_frame()

        display_frame.grid(row=0, column=0, padx=10, pady=10, sticky=N + W)
        bottom_frame.grid(row=1, column=0, padx=10, pady=10, sticky=N + W)
        config_frame.grid(row=2, column=0, padx=10, pady=10, sticky=N + W)

    def task_display_frame(self):
        width = self.windows_size[0] - 20
        height = 130
        frame = Frame(self, width=width, height=height)
        frame.grid_propagate(False)
        frame.columnconfigure(0, weight=width)
        frame.rowconfigure(0, weight=5)
        frame.rowconfigure(1, weight=height - 20)

        title = Label(frame, text="Task: None", width=width, height=5)
        text = Text(frame, width=width, height=height-30)
        title.config(bg='white', anchor=W, justify=LEFT)

        title.grid(row=0, column=0, pady=10, sticky=N + W)
        text.grid(row=1, column=0, sticky=N + W)
        return frame, title, text

    def config_frame(self):
        frame = Frame(self)
        for i in range(len(atf.bot_config_title_fns)):
            title_fns, sub_fns = atf.bot_config_title_fns[i]
            check = section_frame(
                self,
                frame,
                title_fns,
                sub_fns
            )
            check.grid(row=i, column=0, sticky=N + W)
        return frame

    def bottom_frame(self):
        frame = Frame(self)

        def on_click(btn):
            if self.bot_thread is None:

                bot = Bot(self.device)
                self.bot = bot
                bot.config = self.bot_config
                bot.building_pos = self.bot_building_pos

                bot.text_update_event = self.on_task_update
                bot.building_pos_update_event = lambda **kw: write_building_pos(kw['building_pos'], kw['prefix'])

                self.bot_thread = threading.Thread(target=bot.start)
                self.bot_thread.start()
                btn.config(text='STOP')
            elif self.bot_thread is not None:
                stop_thread(self.bot_thread)
                self.bot_thread = None
                self.task_title.config(text='Task: None')
                self.task_text.delete(1.0, END)
                self.bot = None
                btn.config(text='START')
            return

        start_button = button(frame, on_click, text='START')
        start_button.grid(row=0, column=0, sticky=N + W)
        return frame

    def on_task_update(self, text):
        title, text_list = text['title'], text['text_list']
        self.task_title.config(text="Task: " + title)
        self.task_text.delete(1.0, END)
        for t in text_list:
            self.task_text.insert(INSERT, t + '\n')

            # for component in sub_components:


def section_frame(app, parent, title_component_fn, sub_component_fns=[], start_row=0, start_column=0):
    outer_frame = Frame(parent)
    inner_frame = Frame(outer_frame)

    def disable_when_false(checked):
        if checked:
            enableChildren(inner_frame)
        else:
            disableChildren(inner_frame)

    title, variable = title_component_fn(app, outer_frame, disable_when_false)
    title.grid(row=start_row, column=start_column, sticky=N + W)

    inner_frame.grid(row=start_row + 1, column=0, padx=30, pady=0, sticky=N + W)

    for row in range(len(sub_component_fns)):
        component, _ = sub_component_fns[row](app, inner_frame)
        component.grid(row=row, column=0, sticky=N + W)

    if not variable.get():
        disableChildren(inner_frame)
    else:
        enableChildren(inner_frame)

    return outer_frame


def disableChildren(parent):
    children = parent.winfo_children()
    for child in children:
        wtype = child.winfo_class()
        if wtype not in ('Frame', 'Labelframe'):
            child.configure(state='disable')
            if wtype == 'Menubutton':
                child.config(width=8, bg='#F0F0F0')
        else:
            disableChildren(child)


def enableChildren(parent):
    for child in parent.winfo_children():
        wtype = child.winfo_class()
        if wtype not in ('Frame', 'Labelframe'):
            child.configure(state='normal')
            if wtype == 'Menubutton':
                child.config(width=8, bg='white')
        else:
            enableChildren(child)

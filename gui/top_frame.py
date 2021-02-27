from tkinter import Frame, OptionMenu, StringVar, Label, Entry, LabelFrame
from tkinter import N, W, E, S, CENTER, LEFT
from gui.creator import button
from config import write_config

from config import HAO_I, TWO_CAPTCHA, NONE

import config


class TopFrame(Frame):

    def __init__(self, windows, cnf={}, **kwargs):
        Frame.__init__(self, windows, kwargs)
        self.windows_size = [kwargs['width'], kwargs['height']]
        self.setting_btn = None

    def buttons_setup(self, **kwargs):
        setting_btn = button(self, kwargs.get('on_setting_click', lambda v: v), text='Setting')
        setting_btn.grid(row=0, column=0, sticky=N + E)
        self.setting_btn = setting_btn


class SettingFrame(Frame):
    def __init__(self, windows, cnf={}, **kwargs):
        Frame.__init__(self, windows, kwargs)
        self.windows_size = [kwargs['width'], kwargs['height']]

        of = self.option_frame()
        twocaptcha_ef = self.twocaptcha_entries()
        haoi_ef = self.haoi_entries()

        of.grid(row=0, column=0, sticky=N + W, padx=10, pady=(10, 0))
        twocaptcha_ef.grid(row=1, column=0, sticky=N + W, padx=10, pady=(10, 0))
        haoi_ef.grid(row=2, column=0, sticky=N + W, padx=10, pady=(10, 0))


    def option_frame(self):
        f = Frame(self)
        method_label = Label(f, text='Method: ')

        options = [NONE, TWO_CAPTCHA, HAO_I]
        value = config.global_config.method
        variable = StringVar()
        variable.set(value)

        def command(value):
            config.global_config.method = value
            write_config(config.global_config)

        option = OptionMenu(f, variable, *options, command=command)

        method_label.grid(row=0, column=0, sticky=W)
        option.grid(row=0, column=1, sticky=N + W)
        return f

    def haoi_entries(self):

        default_user_key = StringVar()
        default_user_key.set(config.global_config.haoiUser)
        default_software_key = StringVar()
        default_software_key.set(config.global_config.haoiRebate)

        lf = LabelFrame(self, text='haoi')
        ul = Label(lf, text='user key:')
        ue = Entry(lf, textvariable=default_user_key)
        rl = Label(lf, text='software key:')
        re = Entry(lf, textvariable=default_software_key)

        ul.config(width=10, anchor=W, justify=LEFT)
        ue.config(width=53, validate='key', validatecommand=(lf.register(self.creator('haoiUser')), '%P'))
        rl.config(width=10, anchor=W, justify=LEFT,)
        re.config(width=53, validate='key', validatecommand=(lf.register(self.creator('haoiRebate')), '%P'))

        ul.grid(row=0, column=0, sticky=N + W, padx=(10, 10), pady=(10, 0))
        ue.grid(row=0, column=1, sticky=N + W, padx=(0, 10), pady=(10, 0))
        rl.grid(row=1, column=0, sticky=N + W, padx=(10, 10), pady=(0, 10))
        re.grid(row=1, column=1, sticky=N + W, padx=(0, 10), pady=(0, 10))

        return lf

    def twocaptcha_entries(self):

        default_user_key = StringVar()
        default_user_key.set(config.global_config.twocaptchaKey)

        lf = LabelFrame(self, text='2captcha')
        ul = Label(lf, text='user key:')
        ue = Entry(lf, textvariable=default_user_key)

        ul.config(width=10, anchor=W, justify=LEFT)
        ue.config(width=53, validate='key', validatecommand=(lf.register(self.creator('twocaptchaKey')), '%P'))
        ul.grid(row=0, column=0, sticky=N + W, padx=(10, 10), pady=(10, 10))
        ue.grid(row=0, column=1, sticky=N + W, padx=(0, 10), pady=(10, 10))

        return lf

    def creator(self, attr_name):
        def validate_cmd(value):
            if value != getattr(config.global_config, attr_name):
                setattr(config.global_config, attr_name, value)
                write_config(config.global_config)
            return True

        return validate_cmd
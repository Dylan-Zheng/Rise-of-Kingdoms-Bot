from tkinter import *
import json
from utils import resource_path


def button(frame, on_click=lambda v: v, **kwargs):
    btn = Button(frame, **kwargs)

    def command():
        on_click(btn)

    btn.config(command=command)
    return btn


def title_checkbox_creator(name, text):
    def title_checkbox(app, parent, on_click=lambda v: v):
        variable = BooleanVar()
        variable.set(TRUE if getattr(app.bot_config, name) else FALSE)

        def command():
            setattr(app.bot_config, name, variable.get())
            write_config_json(app.bot_config)
            on_click(variable.get())

        checkbox = Checkbutton(
            parent,
            text=text,
            variable=variable,
            command=command
        )
        return checkbox, variable

    return title_checkbox


def train_fn_creator(name, train_attr_name, upgrade_attr_name):
    lv_training_options = ['1', '2', '3', '4', '5', 'Disabled']
    lv_upgrade_options = ['1', '2', '3', '4', '5', 'All', 'Disabled']

    def num_to_option_value(num):
        return str(num + 1 if 0 <= num <= 4 else 'All' if num == 5 else 'Disable')

    def option_value_to_num(v):
        return int(v if v != 'All' and v != 'Disabled' else 6 if v == 'All' else 0) - 1

    def train(app, parent):
        frame = Frame(parent)

        name_tag = Label(frame, text=name)

        def update_command(v):
            setattr(app.bot_config, upgrade_attr_name, option_value_to_num(v))
            write_config_json(app.bot_config)

        upgrade_label = Label(frame, text='Upgrade Lv.')
        upgrade_variable = StringVar()
        upgrade_variable.set(num_to_option_value(getattr(app.bot_config, upgrade_attr_name)))
        upgrade_option = OptionMenu(
            frame,
            upgrade_variable,
            *lv_upgrade_options,
            command=update_command
        )

        def train_command(v):
            setattr(app.bot_config, train_attr_name, option_value_to_num(v))
            write_config_json(app.bot_config)

        train_label = Label(frame, text='Training Lv.')
        train_variable = StringVar()
        train_variable.set(num_to_option_value(getattr(app.bot_config, train_attr_name)))
        train_option = OptionMenu(
            frame,
            train_variable,
            *lv_training_options,
            command=train_command
        )

        name_tag.config(width=8, anchor=N + W, justify=LEFT)
        upgrade_option.config(width=8)
        train_option.config(width=8)

        frame.columnconfigure(0, weight=5)
        name_tag.grid(row=0, column=0)
        train_label.grid(row=0, column=2)
        train_option.grid(row=0, column=3)
        upgrade_label.grid(row=0, column=4)
        upgrade_option.grid(row=0, column=5)

        return frame, None

    return train


def write_config_json(config):
    config_json = json.dumps(config.__dict__)
    with open(resource_path("config.json"), 'w') as f:
        f.write(config_json)

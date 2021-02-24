from gui.creator import *


break_checkbox = checkbox_fn_creator('enableBreak', 'Take break at every end of round')


def time_drop_down(app, parent):
    value = '{} Minute'.format(int(app.bot_config.breakTime / 60))
    options = ['1 Minute', '2 Minute', '3 Minute', '4 Minute', '5 Minute', '10 Minute', '15 Minute', '20 Minute']
    variable = StringVar()
    variable.set(value)

    def command(value):
        app.bot_config.breakTime = int(value.replace(' Minute', '')) * 60

    option = OptionMenu(parent, variable, *options, command=command)
    return option, variable


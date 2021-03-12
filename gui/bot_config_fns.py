from gui.creator import checkbox_fn_creator, train_fn_creator, write_bot_config

from tkinter import StringVar, OptionMenu, Frame, Label, Entry, N, W

import webbrowser

def integer_entry_validate_cmd_creator(app, attr_name, def_value=0):
    def validate_cmd(value, action_type):
        if action_type == '1':
            if not value.isdigit():
                return False
            if len(value) > 1 and value[0] == '0':
                return False
        setattr(app.bot_config, attr_name, int(value if value != '' else str(def_value)))
        write_bot_config(app.bot_config, app.device.serial.replace(':', "_"))
        return True

    return validate_cmd


# break
break_checkbox = checkbox_fn_creator('enableBreak', 'Take break at every end of round')


def time_drop_down(app, parent):
    value = '{} Minute'.format(int(app.bot_config.breakTime / 60))
    options = ['1 Minute', '2 Minute', '3 Minute', '4 Minute', '5 Minute', '10 Minute', '15 Minute', '20 Minute']
    variable = StringVar()
    variable.set(value)

    def command(value):
        app.bot_config.breakTime = int(value.replace(' Minute', '')) * 60
        write_bot_config(app.bot_config, app.device.serial.replace(':', "_"))

    option = OptionMenu(parent, variable, *options, command=command)
    return option, variable


# In city
collecting_checkbox = checkbox_fn_creator('enableCollecting', 'Collecting resource, troops, and help alliance')

produce_material = checkbox_fn_creator('enableMaterialProduce', 'Produce material')

open_free_chest_in_tavern = checkbox_fn_creator('enableTavern', 'Open free chest in tavern')

training = checkbox_fn_creator('enableTraining', 'Auto upgrade and train troops')

train_barracks = train_fn_creator(
    'Barracks:',
    'trainBarracksTrainingLevel',
    'trainBarracksUpgradeLevel')

train_archery_range = train_fn_creator(
    'Archery:',
    'trainArcheryRangeTrainingLevel',
    'trainArcheryRangeUpgradeLevel')

train_stable = train_fn_creator(
    'Stable:',
    'trainStableTrainingLevel',
    'trainStableUpgradeLevel')

train_siege = train_fn_creator(
    'Siege:',
    'trainSiegeWorkshopTrainingLevel',
    'trainSiegeWorkshopUpgradeLevel')

# other
daily_vip_point_and_chest = checkbox_fn_creator('enableVipClaimChest', 'Claim daily vip point and chest')

claim_quest_checkbox = checkbox_fn_creator('claimQuests', 'Claim quests and daily objectives')

alliance_action_checkbox = checkbox_fn_creator('allianceAction',
                                               'Collecting allied resource, gifts, and donate technology')

# Outside

attack_barbarians_checkbox = checkbox_fn_creator('attackBarbarians', 'Attack Barbarians (developing)')


def barbarians_level(app, parent):
    str_value = StringVar()
    str_value.set(str(getattr(app.bot_config, 'barbariansLevel')))

    frame = Frame(parent)
    label = Label(frame, text='Level:')
    entry = Entry(frame, textvariable=str_value)

    def creator(attr_name):
        def validate_cmd(value, action_type):
            if action_type == '1':
                if not value.isdigit():
                    return False
                if value[0] == '0':
                    return False
            setattr(app.bot_config, attr_name, int(value if value != '' else '1'))
            write_bot_config(app.bot_config, app.device.serial.replace(':', "_"))
            return True

        return validate_cmd

    entry.config(width=10, validate='key', validatecommand=(
        frame.register(creator('barbariansLevel')), '%P', '%d'
    ))

    label.grid(row=0, column=0, sticky=N + W, padx=5)
    entry.grid(row=0, column=1, sticky=N + W, padx=5)
    return frame, None


gather_resource_checkbox = checkbox_fn_creator('gatherResource', 'Gather resource')
resource_no_secondery_commander = checkbox_fn_creator('gatherResourceNoSecondaryCommander', 'Not secondary commader')
use_gathering_boosts = checkbox_fn_creator('useGatheringBoosts', 'Use gathering boosts')


def resource_ratio(app, parent):
    label_texts = ['Food:', 'Wood:', 'Stone:', 'Gold:']
    attr_names = ['gatherResourceRatioFood',
                  'gatherResourceRatioWood',
                  'gatherResourceRatioStone',
                  'gatherResourceRatioGold']

    frame = Frame(parent)
    label_1 = Label(frame, text='Type:')
    label_2 = Label(frame, text='Ratio:')
    label_1.grid(row=0, column=0, sticky=N + W, padx=(0, 5))
    label_2.grid(row=1, column=0, sticky=N + W, padx=(0, 5))
    for col in range(4):
        str_value = StringVar()
        str_value.set(str(getattr(app.bot_config, attr_names[col])))

        label = Label(frame, text=label_texts[col])
        entry = Entry(frame, textvariable=str_value)

        def creator(attr_name):
            def validate_cmd(value, action_type):
                if action_type == '1':
                    if not value.isdigit():
                        return False
                    if len(value) > 1 and value[0] == '0':
                        return False
                setattr(app.bot_config, attr_name, int(value if value != '' else '0'))
                write_bot_config(app.bot_config, app.device.serial.replace(':', "_"))
                return True

            return validate_cmd

        entry.config(validate='key', validatecommand=(
            frame.register(creator(attr_names[col])), '%P', '%d'
        ))
        label.grid(row=0, column=col + 1, sticky=N + W, padx=5)
        entry.grid(row=1, column=col + 1, sticky=N + W, padx=5)

        entry.config(width=10)
    return frame, None


bot_config_title_fns = [
    [break_checkbox, [time_drop_down]],
    [collecting_checkbox, []],
    [produce_material, []],
    [open_free_chest_in_tavern, []],
    [daily_vip_point_and_chest, []],
    [claim_quest_checkbox, []],
    [alliance_action_checkbox, []],
    [training, [train_barracks, train_archery_range, train_stable, train_siege]],
    [attack_barbarians_checkbox, [barbarians_level]],
    [gather_resource_checkbox, [use_gathering_boosts, resource_ratio, resource_no_secondery_commander]]
]


def callback(url):
    webbrowser.open_new(url)



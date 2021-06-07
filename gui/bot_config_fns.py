from gui.creator import checkbox_fn_creator, train_fn_creator, write_bot_config, entry_int_fn_creator

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


# restart
restart_checkbox = checkbox_fn_creator('enableStop', 'Auto Restart Game')
restart_do_round = entry_int_fn_creator('stopDoRound', 'Execute at every', 'round')

# break
break_do_round = entry_int_fn_creator('breakDoRound', 'Execute at every', 'round')
terminate_checkbox = checkbox_fn_creator('terminate', 'Terminate when break')
break_checkbox = checkbox_fn_creator('enableBreak', 'Take break at every end of round')

# Mystery Merchant
mystery_merchant_checkbox = checkbox_fn_creator('enableMysteryMerchant', 'Use resource buy item in Mystery Merchant')


def time_drop_down(app, parent):
    value = '{} Minute'.format(int(app.bot_config.breakTime / 60))
    options = [
        '1 Minute',
        '2 Minute',
        '3 Minute',
        '4 Minute',
        '5 Minute',
        '10 Minute',
        '15 Minute',
        '20 Minute',
        '25 Minute',
        '30 Minute',
        '40 Minute',
        '50 Minute',
        '60 Minute'
    ]
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
material_do_round = entry_int_fn_creator('materialDoRound', 'Execute at every', 'round')

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
vip_do_round = entry_int_fn_creator('vipDoRound', 'Execute at every', 'round')

claim_quest_checkbox = checkbox_fn_creator('claimQuests', 'Claim quests and daily objectives')
quest_do_round = entry_int_fn_creator('questDoRound', 'Execute at every', 'round')

alliance_action_checkbox = checkbox_fn_creator('allianceAction',
                                               'Collecting allied resource, gifts, and donate technology')
alliance_do_round = entry_int_fn_creator('allianceDoRound', 'Execute at every', 'round')

# Outside

attack_barbarians_checkbox = checkbox_fn_creator('attackBarbarians', 'Attack Barbarians')
hold_position_checkbox = checkbox_fn_creator('holdPosition', 'Hold Position After Attack')
heal_troops_checkbox = checkbox_fn_creator('healTroopsBeforeAttack', 'Heal Troops Before Attack')
use_daily_ap_checkbox = checkbox_fn_creator('useDailyAPRecovery', 'Use Daily AP Recovery')
use_normal_ap_checkbox = checkbox_fn_creator('useNormalAPRecovery', 'Use Normal AP Recovery')
barbarians_base_level_entry = entry_int_fn_creator('barbariansBaseLevel', 'Base Level(normal/kvk):')
barbarians_min_level_entry = entry_int_fn_creator('barbariansMinLevel', 'Minimum attack Level:')
barbarians_max_level_entry = entry_int_fn_creator('barbariansMaxLevel', 'Maximum attack Level:')
number_of_attack_entry = entry_int_fn_creator('numberOfAttack', 'Number of Attack:')
timeout_entry = entry_int_fn_creator('timeout', 'Timeout (Second):')

gather_resource_checkbox = checkbox_fn_creator('gatherResource', 'Gather resource')
resource_no_secondery_commander = checkbox_fn_creator('gatherResourceNoSecondaryCommander', 'Not secondary commader')
use_gathering_boosts = checkbox_fn_creator('useGatheringBoosts', 'Use gathering boosts')
hold_one_query_space_checkbox = checkbox_fn_creator('holdOneQuerySpace', 'Hold space for attack barbarians')

enable_scout_checkbox = checkbox_fn_creator('enableScout', 'Enable explore')
enable_Investigation_checkbox = checkbox_fn_creator('enableInvestigation', 'Investigate Cave, Village')


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
    # [restart_checkbox, [restart_do_round]],
    [break_checkbox, [break_do_round, terminate_checkbox, time_drop_down]],
    [mystery_merchant_checkbox, []],
    [open_free_chest_in_tavern, []],
    [collecting_checkbox, []],
    [produce_material, [material_do_round]],
    [daily_vip_point_and_chest, [vip_do_round]],
    [claim_quest_checkbox, [quest_do_round]],
    [alliance_action_checkbox, [alliance_do_round]],
    [training, [train_barracks, train_archery_range, train_stable, train_siege]],
    [attack_barbarians_checkbox, [hold_position_checkbox,
                                  heal_troops_checkbox,
                                  use_daily_ap_checkbox,
                                  use_normal_ap_checkbox,
                                  barbarians_base_level_entry,
                                  barbarians_min_level_entry,
                                  barbarians_max_level_entry,
                                  number_of_attack_entry,
                                  timeout_entry]],
    [gather_resource_checkbox, [use_gathering_boosts, hold_one_query_space_checkbox, resource_ratio, resource_no_secondery_commander]],
    [enable_scout_checkbox, [enable_Investigation_checkbox]]
]


def callback(url):
    webbrowser.open_new(url)

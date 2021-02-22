from gui.creator import *

# break
break_checkbox = title_checkbox_creator('enableBreak', 'Take break at every end of round')


def time_drop_down(app, parent):
    value = '{} Minute'.format(int(app.bot_config.breakTime / 60))
    options = ['1 Minute', '2 Minute', '3 Minute', '4 Minute', '5 Minute', '10 Minute', '15 Minute', '20 Minute']
    variable = StringVar()
    variable.set(value)

    def command(value):
        app.bot_config.breakTime = int(value.replace(' Minute', '')) * 60

    option = OptionMenu(parent, variable, *options, command=command)
    return option, variable


# In city
collecting_checkbox = title_checkbox_creator('enableCollecting', 'Collecting resource, troops, and help alliance')

produce_material = title_checkbox_creator('enableMaterialProduce', 'Produce material')

open_free_chest_in_tavern = title_checkbox_creator('enableTavern', 'Open free chest in tavern')

training = title_checkbox_creator('enableTraining', 'Auto upgrade and train troops')

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
claim_quest_checkbox = title_checkbox_creator('claimQuests', 'Claim quests and daily objectives')

alliance_action_checkbox = title_checkbox_creator('allianceAction', 'Collecting allied resource, gifts, and donate technology')

# Outside
gather_resource_checkbox = title_checkbox_creator('gatherResource', 'Gather resource')


title_fns = [
    [break_checkbox, [time_drop_down]],
    [collecting_checkbox, []],
    [produce_material, []],
    [open_free_chest_in_tavern, []],
    [training, [train_barracks, train_archery_range, train_stable, train_siege]],
    [claim_quest_checkbox, []],
    [alliance_action_checkbox, []],
    [gather_resource_checkbox, []]

]






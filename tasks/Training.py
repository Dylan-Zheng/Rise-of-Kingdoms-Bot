import traceback

from bot_related.bot_config import TrainingAndUpgradeLevel
from filepath.file_relative_paths import ImagePathAndProps
from tasks.constants import BuildingNames
from tasks.constants import TaskName
from tasks.Task import Task


class Training(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.GATHER):
        super().set_text(title='Train and Upgrade Troops', remove=True)
        super().set_text(insert='Init view')
        super().back_to_map_gui()
        super().back_to_home_gui()
        super().home_gui_full_view()
        try:
            soldier_icon_pos = [
                (630, 175),
                (730, 175),
                (830, 175),
                (930, 175),
                (1030, 175),
            ]

            for config in [
                [
                    ImagePathAndProps.BARRACKS_BUTTON_IMAGE_PATH.value,
                    self.bot.config.trainBarracksTrainingLevel,
                    self.bot.config.trainBarracksUpgradeLevel,
                    self.bot.building_pos[BuildingNames.BARRACKS.value],
                    BuildingNames.BARRACKS.value,
                ],
                [
                    ImagePathAndProps.ARCHER_RANGE_BUTTON_IMAGE_PATH.value,
                    self.bot.config.trainArcheryRangeTrainingLevel,
                    self.bot.config.trainArcheryRangeUpgradeLevel,
                    self.bot.building_pos[BuildingNames.ARCHERY_RANGE.value],
                    BuildingNames.ARCHERY_RANGE.value
                ],
                [
                    ImagePathAndProps.STABLE_BUTTON_IMAGE_PATH.value,
                    self.bot.config.trainStableTrainingLevel,
                    self.bot.config.trainStableUpgradeLevel,
                    self.bot.building_pos[BuildingNames.STABLE.value],
                    BuildingNames.STABLE.value,
                ],
                [
                    ImagePathAndProps.SIEGE_WORKSHOP_BUTTON_IMAGE_PATH.value,
                    self.bot.config.trainSiegeWorkshopTrainingLevel,
                    self.bot.config.trainSiegeWorkshopUpgradeLevel,
                    self.bot.building_pos[BuildingNames.SIEGE_WORKSHOP.value],
                    BuildingNames.SIEGE_WORKSHOP.value
                ]
            ]:
                super().set_text(insert='Train or upgrade troops({})'.format(config[4]))
                super().back_to_home_gui()
                upgraded = False
                x, y = config[3]
                super().tap(x, y, 1)
                _, _, pos = self.gui.check_any(config[0])
                if pos is None:
                    continue
                x, y = pos
                super().tap(x, y, 1)
                _, _, pos = self.gui.check_any(ImagePathAndProps.SPEED_UP_BUTTON_IMAGE_PATH.value)
                if pos is not None:
                    continue
                if config[2] != TrainingAndUpgradeLevel.DISABLED.value:
                    max = config[2] if config[2] != TrainingAndUpgradeLevel.UPGRADE_ALL.value \
                        else TrainingAndUpgradeLevel.T4.value
                    min = config[2] - 1 if config[2] != TrainingAndUpgradeLevel.UPGRADE_ALL.value else -1
                    for i in range(max, min, -1):
                        x, y = soldier_icon_pos[i]
                        super().tap(x, y, 0.5)
                        # check has upgrade button, if has then tap it
                        _, _, pos = self.gui.check_any(ImagePathAndProps.TRAINING_UPGRADE_BUTTON_IMAGE_PATH.value)
                        if pos is None:
                            if config[2] != TrainingAndUpgradeLevel.UPGRADE_ALL.value:
                                break
                            else:
                                continue
                        x, y = pos
                        super().set_text(insert='Upgrade T{}({})'.format(i + 1, config[4]))
                        super().tap(x, y, 0.5)

                        # check has train button if has then tap it
                        _, _, pos = self.gui.check_any(ImagePathAndProps.UPGRADE_BUTTON_IMAGE_PATH.value)
                        x, y = pos
                        super().tap(x, y, 0.5)
                        upgraded = True

                if not upgraded and (
                        config[1] != TrainingAndUpgradeLevel.DISABLED.value):
                    for i in range(config[1], -1, -1):
                        x, y = soldier_icon_pos[i]
                        super().tap(x, y, 0.5)
                        _, _, pos = self.gui.check_any(ImagePathAndProps.TRAIN_BUTTON_IMAGE_PATH.value)
                        if pos is None:
                            continue
                        super().set_text(insert='Train T{}({})'.format(i + 1, config[4]))
                        x, y = pos
                        super().tap(x, y, 0.5)
                        break
        except Exception as e:
            traceback.print_exc()
            return TaskName.TRAINING
        return next_task

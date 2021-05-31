import traceback

from filepath.file_relative_paths import ImagePathAndProps
from tasks.constants import BuildingNames
from tasks.constants import TaskName
from tasks.Task import Task


class Tavern(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.TRAINING):
        super().set_text(title='Tavern', remove=True)
        super().set_text(insert='Init view')
        super().back_to_home_gui()
        super().home_gui_full_view()
        tavern_pos = self.bot.building_pos[BuildingNames.TAVERN.value]

        # tap tavern building
        x, y = tavern_pos
        super().set_text(insert='Tap tavern at position ({}, {})'.format(x, y))
        super().tap(x, y, 1)
        _, _, tavern_btn_pos = self.gui.check_any(ImagePathAndProps.TAVERN_BUTTON_BUTTON_IMAGE_PATH.value)
        if tavern_btn_pos is None:
            return next_task
        x, y = tavern_btn_pos
        super().tap(x, y, 4)
        for i in range(20):
            _, _, open_btn_pos = self.gui.check_any(ImagePathAndProps.CHEST_OPEN_BUTTON_IMAGE_PATH.value)
            if open_btn_pos is None:
                return next_task
            x, y = open_btn_pos
            super().set_text(insert="Tap open button at ({}, {})".format(x, y))
            super().tap(x, y, 4)
            _, _, confirm_btn_pos = self.gui.check_any(ImagePathAndProps.CHEST_CONFIRM_BUTTON_IMAGE_PATH.value)
            if confirm_btn_pos is None:
                return next_task
            x, y = confirm_btn_pos
            super().tap(x, y, 4)
        return next_task

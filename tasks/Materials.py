import traceback

from filepath.file_relative_paths import ImagePathAndProps
from tasks.constants import BuildingNames
from tasks.constants import TaskName
from tasks.Task import Task


class Materials(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.TAVERN):
        try:
            super().set_text(title='Materials Production', remove=True)

            icon_pos = [
                (765, 230),
                (860, 230),
                (950, 230),
                (1045, 230)
            ]
            super().set_text(insert='Init view')
            super().back_to_home_gui()
            super().home_gui_full_view()
            blacksmith_pos = self.bot.building_pos[BuildingNames.BLACKSMITH.value]
            x, y = blacksmith_pos
            super().tap(x, y, 2)
            _, _, product_btn_pos = self.gui.check_any(ImagePathAndProps.MATERIALS_PRODUCTION_BUTTON_IMAGE_PATH.value)
            if product_btn_pos is None:
                return next_task
            x, y = product_btn_pos
            super().tap(x, y, 5)
            list_amount = self.gui.materilal_amount_image_to_string()
            super().set_text(insert='\nLeather: {}\nIton: {}\nEboy: {}\nBone: {}'.format(
                list_amount[0], list_amount[1], list_amount[2], list_amount[3])
            )
            min = 0
            for i in range(len(list_amount)):
                if list_amount[min] > list_amount[i]:
                    min = i
            x, y = icon_pos[min]
            super().set_text(insert='Produce least material')
            for i in range(5):
                super().tap(x, y, 0.5)
        except Exception as e:
            traceback.print_exc()
            return next_task
        return next_task
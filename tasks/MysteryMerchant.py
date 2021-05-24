from filepath.file_relative_paths import ImagePathAndProps
from tasks.Task import Task
import traceback

from tasks.constants import TaskName


class MysteryMerchant(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.MYSTERY_MERCHANT.value):
        self.set_text(title='Mystery Merchant')
        self.back_to_home_gui()
        self.home_gui_full_view()

        found, _, pos = self.gui.check_any(ImagePathAndProps.MERCHANT_ICON_IMAGE_PATH.value)
        if not found:
            self.set_text(insert='Mystery Merchant not found', index=0)
            return next_task
        self.set_text(insert='Open Mystery Merchant')
        x, y = pos
        self.tap(x, y, 2)

        while True:

            for i in range(5):

                self.set_text(insert='buy item with food')
                list = self.gui.find_all_image_props(ImagePathAndProps.MERCHANT_BUY_WITH_FOOD_IMAGE_PATH.value)
                for buy_with_food_btn in list:
                    x, y = buy_with_food_btn['result']
                    self.tap(x, y, 0.5)

                self.set_text(insert='buy item with wood')
                list = self.gui.find_all_image_props(ImagePathAndProps.MERCHANT_BUY_WITH_WOOD_IMAGE_PATH.value)
                for buy_with_wood_btn in list:
                    x, y = buy_with_wood_btn['result']
                    self.tap(x, y, 0.5)

                self.swipe(730, 575, 730, 475, 1, 1000)

            # tap on free refresh
            found, _, pos = self.gui.check_any(ImagePathAndProps.MERCHANT_FREE_BTN_IMAGE_PATH.value)
            if not found:
                return next_task
            self.set_text(insert='Refresh')
            x, y = pos
            self.tap(x, y, 2)



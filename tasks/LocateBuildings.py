import math
import time

from filepath.file_relative_paths import ImagePathAndProps
from tasks.Task import Task
import traceback

from tasks.constants import TaskName, DEFAULT_RESOLUTION


class LocateBuilding(Task):
    def __init__(self, bot):
        super().__init__(bot)

        # screen range x0 250, x1 950, y0 95, y1 615

    def do(self, next_task=TaskName.COLLECTING):

        try:
            super().set_text(title='Init Building Position', remove=True)
            super().set_text(insert='progress: 0%', index=0)
            super().set_text(append='init view')

            super().back_to_home_gui()
            super().home_gui_full_view()

            # close menu
            super().menu_should_open(False)

            if self.bot.config.hasBuildingPos:
                super().curr_task = TaskName.NEXT_TASK
                return

            width = DEFAULT_RESOLUTION['width']
            height = DEFAULT_RESOLUTION['height']

            x0 = 250
            x1 = 950
            y0 = 95
            y1 = 615

            x_times = 12
            y_times = 10

            x_interval = math.floor((x1 - x0) / (x_times - 1))
            y_interval = math.floor((y1 - y0) / y_times)

            x_start = x0
            y_start = y0

            x_end = x1
            y_end = y1

            total = x_times * y_times

            # tap every point to get building position
            for row in range(0, y_times):
                for col in range(0, x_times):
                    x, y = x_start + x_interval * col, y_start + y_interval * row
                    super().tap(x, y, 1)
                    super().set_text(insert='tap at ({}, {})'.format(x, y), index=1)
                    num_of_back = super().back_to_home_gui()
                    if num_of_back == 0:
                        super().tap(x_start, y_start)
                        super().tap(x, y)

                    # sleep 0.5 sec just for a case if screen print before button display
                    time.sleep(0.5)
                    # check is tap on building
                    has_info_btn, _, info_btn_pos = self.gui.check_any(
                        ImagePathAndProps.BUILDING_INFO_BUTTON_IMG_PATH.value)

                    # if tap on the building, then try to tap on building infomation button to get building name
                    if has_info_btn:
                        x, y = info_btn_pos
                        super().tap(x, y, 1)
                        name = self.gui.get_windows_name()
                        if name is None:
                            super().back_to_home_gui()
                        else:
                            name = name.lower()
                            level = 0
                            if 'level ' in name:
                                level, name = name.replace('level ', '').split(' ', 1)
                            self.bot.building_pos[name.replace(' ', '_')] = (x, y)
                            super().set_text(insert='<{}> on position ({}, {})'.format(name, x, y), index=1)
                            super().back()

                    super().tap(x_start, y_start)
                    super().set_text(
                        replace='progress: {}%'.format(int(((row * x_times) + (col + 1)) / total * 100)),
                        index=0)

            # save building pos to json
            self.bot.config.hasBuildingPos = True
            self.bot.building_pos_update_event(building_pos=self.bot.building_pos,
                                              prefix=self.device.serial.replace(':', "_"))
            self.bot.config_update_event(config=self.bot.config, prefix=super().device.serial.replace(':', "_"))
        except Exception as e:
            traceback.print_exc()
            self.bot.config.hasBuildingPos = False
            return TaskName.INIT_BUILDING_POS
        return next_task

import traceback
import time

from filepath.file_relative_paths import ImagePathAndProps
from tasks.constants import TaskName, BuildingNames
from tasks.Task import Task


class Scout(Task):
    def __init__(self, bot):
        super().__init__(bot)
        with open("resource/cavelist.txt") as file:
            self.lines = [line.rstrip() for line in file]

    def click_on_cave(self):
        idx = 0
        result_list = self.gui.find_all_image_props(
                        ImagePathAndProps.CAVE_IMG_PATH.value
                    )
        result_list.sort(key=lambda result: result['result'][1])
        print(len(result_list))
        if idx < len(result_list):
            x, y = result_list[idx]['result']
            print(x,y)
            self.tap(x, y, 2)
    
    def goto_cave(self, cx, cy):
        coord = {
            "magifier" : (440, 22),
            "cavexinput": (608, 145),
            "caveyinput" : (762, 145),
            "gotocave" : (888, 145)
        }
        #coord = [(440, 22), (608, 145), (762, 145), (888, 145)]
        x, y = coord["magifier"]
        self.tap(x, y, 2)
        x, y = coord["cavexinput"]
        self.tap(x, y, 2)
        self.input(cx, 2)
        self.tap(x, y, 2)
        x, y = coord["caveyinput"]
        self.tap(x, y, 2)
        self.input(cy, 2)
        self.tap(x, y, 2)
        x, y = coord["gotocave"]
        self.tap(x, y, 2)


    def do(self, next_task=TaskName.BREAK):
        coord_input_pos = (60, 540)
        coord_x_pos = ()
        coord_y_pos = ()
        self.back_to_map_gui()
        try:
            self.set_text(title='Auto Scout')
            for line in self.lines:
                cx, cy, ctype = line.split(",")
                self.set_text(insert = line)
                self.back_to_map_gui()
                self.goto_cave(cx, cy)
                self.click_on_cave()
                time.sleep(10)
            return next_task
        except Exception as e:
            traceback.print_exc()
            return next_task


        try:
            self.set_text(title='Auto Scout')
            mail_pos = [1230, 570]
            report_pos = [250, 45]
            center_pos = (640, 320)

            idx = 0
            while self.bot.config.enableInvestigation:
                self.back_to_map_gui()
                self.set_text(insert='Open mail')
                x, y = mail_pos
                self.tap(x, y, 2)
                self.set_text(insert='Open report')
                x, y = report_pos
                self.tap(x, y, 1)

                found, name, pos = self.gui.check_any(
                    ImagePathAndProps.MAIL_EXPLORATION_REPORT_IMAGE_PATH.value,
                    ImagePathAndProps.MAIL_SCOUT_BUTTON_IMAGE_PATH.value
                )

                if found:
                    if name == ImagePathAndProps.MAIL_EXPLORATION_REPORT_IMAGE_PATH.value[5]:
                        x, y = pos
                        self.tap(x, y, 2)

                    result_list = self.gui.find_all_image_props(
                        ImagePathAndProps.MAIL_SCOUT_BUTTON_IMAGE_PATH.value
                    )
                    result_list.sort(key=lambda result: result['result'][1])

                    if idx < len(result_list):
                        x, y = result_list[idx]['result']
                        self.tap(x, y, 2)
                    else:
                        break

                    x, y = pos
                    self.tap(x, y, 2)

                else:
                    break

                x, y = center_pos
                self.tap(x, y, 0.1)
                self.tap(x, y, 0.1)
                self.tap(x, y, 0.1)
                self.tap(x, y, 0.1)
                self.tap(x, y, 0.5)

                found, name, pos = self.gui.check_any(
                    ImagePathAndProps.INVESTIGATE_BUTTON_IMAGE_PATH.value,
                    ImagePathAndProps.GREAT_BUTTON_IMAGE_PATH.value
                )

                if found:
                    x, y = pos
                    self.tap(x, y, 2)
                else:
                    continue

                if name == ImagePathAndProps.INVESTIGATE_BUTTON_IMAGE_PATH.value[5]:

                    found, name, pos = self.gui.check_any(
                        ImagePathAndProps.SCOUT_IDLE_ICON_IMAGE_PATH.value,
                        ImagePathAndProps.SCOUT_ZZ_ICON_IMAGE_PATH.value
                    )

                    if found:
                        x, y = pos
                        self.tap(x - 10, y - 10, 2)
                    else:
                        break

                    found, name, pos = self.gui.check_any(
                        ImagePathAndProps.SCOUT_SEND_BUTTON_IMAGE_PATH.value,
                    )

                    if found:
                        x, y = pos
                        self.tap(x, y, 2)
                    else:
                        break
                else:
                    continue

                idx = idx + 1

            while True:
                self.set_text(insert='init view')
                self.back_to_home_gui()
                self.home_gui_full_view()

                # open scout interface
                self.set_text(insert='tap scout camp')
                scout_camp_pos = self.bot.building_pos[BuildingNames.SCOUT_CAMP.value]
                x, y = scout_camp_pos
                self.tap(x, y, 1)

                # find and tap scout button
                self.set_text(insert='open scout camp')
                is_found, _, btn_pos = self.gui.check_any(
                    ImagePathAndProps.SCOUT_BUTTON_IMAGE_PATH.value
                )
                if is_found:
                    x, y = btn_pos
                    self.tap(x, y, 1)
                else:
                    return next_task

                # find and tap explore button
                self.set_text(insert='try to tap explore')
                is_found, _, btn_pos = self.gui.check_any(
                    ImagePathAndProps.SCOUT_EXPLORE_BUTTON_IMAGE_PATH.value
                )
                if is_found:
                    x, y = btn_pos
                    self.tap(x, y, 2)
                else:
                    return next_task

                # find and tap explore button
                self.set_text(insert='try to tap explore')
                is_found, _, btn_pos = self.gui.check_any(
                    ImagePathAndProps.SCOUT_EXPLORE2_BUTTON_IMAGE_PATH.value
                )
                if is_found:
                    x, y = btn_pos
                    self.tap(x, y, 2)
                else:
                    return next_task

                self.set_text(insert='try to tap send')

                found, name, pos = self.gui.check_any(
                    ImagePathAndProps.SCOUT_IDLE_ICON_IMAGE_PATH.value,
                    ImagePathAndProps.SCOUT_ZZ_ICON_IMAGE_PATH.value
                )
                if found:
                    x, y = pos
                    self.tap(x - 10, y - 10, 2)
                else:
                    return next_task

                is_found, _, btn_pos = self.gui.check_any(
                    ImagePathAndProps.SCOUT_SEND_BUTTON_IMAGE_PATH.value
                )
                if is_found:
                    x, y = btn_pos
                    self.tap(x, y, 2)
                else:
                    return next_task
        except Exception as e:
            traceback.print_exc()
            return next_task

        return next_task

import traceback

from filepath.file_relative_paths import ImagePathAndProps
from tasks.constants import TaskName, BuildingNames
from tasks.Task import Task


class Scout(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.BREAK):

        try:
            super().set_text(title='Auto Scout')
            mail_pos = [1230, 570]
            center_pos = (640, 320)

            idx = 0
            while self.bot.config.enableInvestigation:
                super().back_to_map_gui()
                super().set_text(insert='Open mail')
                x, y = mail_pos
                super().tap(x, y, 2)

                found, name, pos = self.gui.check_any(
                    ImagePathAndProps.MAIL_EXPLORATION_REPORT_IMAGE_PATH.value,
                    ImagePathAndProps.MAIL_SCOUT_BUTTON_IMAGE_PATH.value
                )

                if found:
                    if name == ImagePathAndProps.MAIL_EXPLORATION_REPORT_IMAGE_PATH.value[5]:
                        x, y = pos
                        super().tap(x, y, 2)

                    result_list = self.gui.find_all_image_props(
                        ImagePathAndProps.MAIL_SCOUT_BUTTON_IMAGE_PATH.value
                    )
                    result_list.sort(key=lambda result: result['result'][1])

                    if idx < len(result_list):
                        x, y = result_list[idx]['result']
                        super().tap(x, y, 2)
                    else:
                        break

                    x, y = pos
                    super().tap(x, y, 2)

                else:
                    break

                x, y = center_pos
                super().tap(x, y, 0.1)
                super().tap(x, y, 0.1)
                super().tap(x, y, 0.1)
                super().tap(x, y, 0.1)
                super().tap(x, y, 0.5)

                found, name, pos = self.gui.check_any(
                    ImagePathAndProps.INVESTIGATE_BUTTON_IMAGE_PATH.value,
                    ImagePathAndProps.GREAT_BUTTON_IMAGE_PATH.value
                )

                if found:
                    x, y = pos
                    super().tap(x, y, 2)
                else:
                    continue

                if name == ImagePathAndProps.INVESTIGATE_BUTTON_IMAGE_PATH.value[5]:

                    found, name, pos = self.gui.check_any(
                        ImagePathAndProps.SCOUT_IDLE_ICON_IMAGE_PATH.value,
                        ImagePathAndProps.SCOUT_ZZ_ICON_IMAGE_PATH.value
                    )

                    if found:
                        x, y = pos
                        super().tap(x - 10, y - 10, 2)
                    else:
                        break

                    found, name, pos = self.gui.check_any(
                        ImagePathAndProps.SCOUT_SEND_BUTTON_IMAGE_PATH.value,
                    )

                    if found:
                        x, y = pos
                        super().tap(x, y, 2)
                    else:
                        break
                else:
                    continue

                idx = idx + 1

            while True:
                super().set_text(insert='init view')
                super().back_to_home_gui()
                super().home_gui_full_view()

                # open scout interface
                super().set_text(insert='tap scout camp')
                scout_camp_pos = self.bot.building_pos[BuildingNames.SCOUT_CAMP.value]
                x, y = scout_camp_pos
                super().tap(x, y, 1)

                # find and tap scout button
                super().set_text(insert='open scout camp')
                is_found, _, btn_pos = self.gui.check_any(
                    ImagePathAndProps.SCOUT_BUTTON_IMAGE_PATH.value
                )
                if is_found:
                    x, y = btn_pos
                    super().tap(x, y, 1)
                else:
                    return next_task

                # find and tap explore button
                super().set_text(insert='try to tap explore')
                is_found, _, btn_pos = self.gui.check_any(
                    ImagePathAndProps.SCOUT_EXPLORE_BUTTON_IMAGE_PATH.value
                )
                if is_found:
                    x, y = btn_pos
                    super().tap(x, y, 2)
                else:
                    return next_task

                # find and tap explore button
                super().set_text(insert='try to tap explore')
                is_found, _, btn_pos = self.gui.check_any(
                    ImagePathAndProps.SCOUT_EXPLORE2_BUTTON_IMAGE_PATH.value
                )
                if is_found:
                    x, y = btn_pos
                    super().tap(x, y, 2)
                else:
                    return next_task

                super().set_text(insert='try to tap send')

                found, name, pos = self.gui.check_any(
                    ImagePathAndProps.SCOUT_IDLE_ICON_IMAGE_PATH.value,
                    ImagePathAndProps.SCOUT_ZZ_ICON_IMAGE_PATH.value
                )
                if found:
                    x, y = pos
                    super().tap(x - 10, y - 10, 2)
                else:
                    return next_task

                is_found, _, btn_pos = self.gui.check_any(
                    ImagePathAndProps.SCOUT_SEND_BUTTON_IMAGE_PATH.value
                )
                if is_found:
                    x, y = btn_pos
                    super().tap(x, y, 2)
                else:
                    return next_task
        except Exception as e:
            traceback.print_exc()
            return next_task

        return next_task

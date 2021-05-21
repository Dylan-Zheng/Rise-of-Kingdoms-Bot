import traceback
import random
import time

from filepath.constants import DEFEAT_MAIL, VICTORY_MAIL, WINDOW
from filepath.file_relative_paths import ImagePathAndProps
from tasks.constants import TaskName
from tasks.Task import Task


class Barbarians(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.GATHER):
        icon_pos = (255, 640)
        center_pos = (640, 320)
        queue_one_pos = (1205, 205, 1235, 230)

        min_lv = self.bot.config.barbariansMinLevel
        max_lv = self.bot.config.barbariansMaxLevel
        base_lv = self.bot.config.barbariansBaseLevel

        try:

            super().set_text(title='Attack Barbarians', remove=True)
            commander_cv_img = None

            is_in_city = True

            for r in range(self.bot.config.numberOfAttack):

                if min_lv < base_lv:
                    min_lv = base_lv

                if min_lv > max_lv | max_lv < base_lv:
                    return next_task

                super().set_text(insert="Attack Round [{}]".format(r + 1))
                if self.bot.config.healTroopsBeforeAttack or r == 0:
                    super().heal_troops()
                super().set_text(insert="Search barbarians")
                super().back_to_map_gui()

                # tap on magnifier
                super().tap(60, 540, 1)
                # tap on barbarians icon
                x, y = icon_pos
                super().tap(x, y, 1)

                # set barbarians level
                level = random.randrange(min_lv, max_lv + 1)
                super().set_text(insert="Select Level is {}".format(level))
                self.set_barbarians_level(level)

                # tap search button
                _, _, search_pos = self.gui.check_any(ImagePathAndProps.RESOURCE_SEARCH_BUTTON_IMAGE_PATH.value)
                x, y = search_pos
                super().tap(x, y, 2)
                x, y = center_pos
                super().tap(x, y, 1)

                found, _, _ = self.gui.check_any(ImagePathAndProps.RESOURCE_SEARCH_BUTTON_IMAGE_PATH.value)
                if found:
                    min_lv = min_lv + 1
                    continue

                # hold position
                self.hold_pos_after_attack(self.bot.config.holdPosition)

                # tap attack button
                _, _, atk_btn_pos = self.gui.check_any(ImagePathAndProps.ATTACK_BUTTON_POS_IMAGE_PATH.value)
                x, y = atk_btn_pos
                super().tap(x, y, 3)

                if not self.bot.config.holdPosition or is_in_city:
                    # tap on new troop
                    has_new_troops_btn, _, new_troop_btn_pos = self.gui.check_any(
                        ImagePathAndProps.NEW_TROOPS_BUTTON_IMAGE_PATH.value)
                    if not has_new_troops_btn:
                        super().set_text(insert="Not more space for march")
                        return next_task
                    x, y = new_troop_btn_pos
                    super().tap(x, y, 2)

                    # select saves
                    self.select_save_blue_one()

                    # start attack
                    _, _, match_button_pos = self.gui.check_any(
                        ImagePathAndProps.TROOPS_MATCH_BUTTON_IMAGE_PATH.value)
                    super().set_text(insert="March")
                    x, y = match_button_pos
                    super().tap(x, y, 1)

                    if self.use_ap_recovery():
                        _, _, match_button_pos = self.gui.check_any(
                            ImagePathAndProps.TROOPS_MATCH_BUTTON_IMAGE_PATH.value)
                        super().set_text(insert="March")
                        x, y = match_button_pos
                        super().tap(x, y, 1)

                    commander_cv_img = self.gui.get_image_in_box(queue_one_pos)
                    is_in_city = False

                else:
                    # find commander and tap it
                    _, _, pos = self.gui.check_any(ImagePathAndProps.HOLD_ICON_IMAGE_PATH.value)

                    if pos is None:
                        break;
                    x, y = pos
                    super().tap(x - 10, y - 10, 2)

                    # tap on match button
                    _, _, pos = self.gui.check_any(ImagePathAndProps.MARCH_BAR_IMAGE_PATH.value)
                    x, y = pos
                    super().tap(x, y, 1)
                    if self.use_ap_recovery():
                        _, _, pos = self.gui.check_any(ImagePathAndProps.MARCH_BAR_IMAGE_PATH.value)
                        x, y = pos
                        super().tap(x, y, 1)

                # block and try to catch battle result
                battle_result = self.battle_result_detector(commander_cv_img)
                if battle_result is None:
                    break
                elif battle_result == DEFEAT_MAIL:
                    if not self.wait_for_commander_back_to_city(commander_cv_img):
                        break
                    is_in_city = True
                    continue
                elif battle_result == VICTORY_MAIL:
                    if not self.bot.config.holdPosition:
                        if not self.wait_for_commander_back_to_city(commander_cv_img):
                            break
                        is_in_city = True
                    else:
                        is_in_city = False
                    continue
                else:
                    break

            # call commander return
            result = self.gui.has_image_cv_img(commander_cv_img)
            if result is not None:
                x, y = result['result']
                super().tap(x, y, 1)
                x, y = center_pos
                super().tap(x, y, 1)
                _, _, pos = self.gui.check_any(ImagePathAndProps.RETURN_BUTTON_IMAGE_PATH.value)
                if pos is not None:
                    x, y = pos
                    super().tap(x, y, 1)
                    is_in_city = True

        except Exception as e:
            traceback.print_exc()
            return next_task

        return next_task

    def set_barbarians_level(self, level):
        max_pos = (375, 405)
        min_pos = (168, 405)
        base_level = self.bot.config.barbariansBaseLevel - 1

        _, _, dec_pos = self.gui.check_any(ImagePathAndProps.DECREASING_BUTTON_IMAGE_PATH.value)
        has_inc_btn, _, inc_pos = self.gui.check_any(ImagePathAndProps.INCREASING_BUTTON_IMAGE_PATH.value)
        _, _, lock_pos = self.gui.check_any(ImagePathAndProps.LOCK_BUTTON_IMAGE_PATH.value)

        curr_lv = self.gui.barbarians_level_image_to_string()
        if curr_lv == level:
            return

        if not has_inc_btn:
            inc_pos = lock_pos

        # set to max level
        x, y = max_pos
        super().swipe(x, y, x + 100, y)
        # try to get max lv. in integer
        max_lv = self.gui.barbarians_level_image_to_string()
        super().set_text(insert="Max level is {}".format(max_lv))
        if max_lv != -1:
            x = max_pos[0] if level > max_pos[0] or level >= 99 else ((level - base_level) / (max_lv - base_level)) * (max_pos[0] - min_pos[0]) + \
                                                                     min_pos[0]
            y = max_pos[1]
            super().tap(x, y, 1)
            # self.gui.debug = True
            curr_lv = self.gui.barbarians_level_image_to_string()
            # self.gui.debug = False

            if curr_lv == -1:
                super().set_text(insert="Fail to read current level, set to lv.1".format(curr_lv))
                x, y = min_pos
                super().tap(x, y, 1)
                curr_lv = 1
            elif abs(level - curr_lv) > 5:
                super().set_text(insert="current level is {}".format(curr_lv))
                super().set_text(insert="fail to read level, set to level 1")
                x, y = min_pos
                super().tap(x, y, 1)
                curr_lv = base_level + 1
            else:
                super().set_text(insert="current level is {}".format(curr_lv))

            btn_pos = inc_pos if curr_lv < level else dec_pos
            for i in range(int(abs(level - curr_lv))):
                x, y = btn_pos
                super().tap(x, y)

    # attack barbarians
    def hold_pos_after_attack(self, should_hold):
        is_check, _, pos = self.gui.check_any(ImagePathAndProps.HOLD_POS_CHECKED_IMAGE_PATH.value)
        if should_hold and not is_check:
            _, _, pos = self.gui.check_any(ImagePathAndProps.HOLD_POS_UNCHECK_IMAGE_PATH.value)
            x, y = pos
            super().tap(x - 3, y)
        elif not should_hold and is_check:
            x, y = pos
            super().tap(x - 3, y)

    def tap_on_save_btn(self, pos):
        _x, _y = pos
        super().tap(_x, _y, 1)
        is_save_unselect, _, _ = self.gui.check_any(
            ImagePathAndProps.UNSELECT_BLUE_ONE_SAVE_BUTTON_IMAGE_PATH.value)
        if is_save_unselect:
            super().set_text(insert='Commander not in city, stop current task')
            raise RuntimeError('Commander not in city, stop current task')

    def select_save_blue_one(self):

        # if blue save one not exist, try to find switch button
        has_save_btn, _, save_btn_pos = self.gui.check_any(
            ImagePathAndProps.UNSELECT_BLUE_ONE_SAVE_BUTTON_IMAGE_PATH.value)

        if not has_save_btn:
            has_switch_btn, _, switch_btn_pos = self.gui.check_any(
                ImagePathAndProps.SAVE_SWITCH_BUTTON_IMAGE_PATH.value)
            # if switch button found tap it to find blue one
            if has_switch_btn:
                for times in range(3):
                    # tap switch button
                    x, y = switch_btn_pos
                    super().tap(x, y)
                    # check is save one exists
                    has_save_btn, _, save_btn_pos = self.gui.check_any(
                        ImagePathAndProps.UNSELECT_BLUE_ONE_SAVE_BUTTON_IMAGE_PATH.value)
                    # if exists tap it else continue
        if has_save_btn:
            self.tap_on_save_btn(save_btn_pos)
        else:
            super().set_text(insert='Save not found')
            raise RuntimeError('Save not found')

    def battle_result_detector(self, commander_cv_img):
        start = time.time()
        super().set_text(insert='Waiting: 0/{}'.format(self.bot.config.timeout))
        while True:
            found, name, pos = self.gui.check_any(
                ImagePathAndProps.VICTORY_MAIL_IMAGE_PATH.value,
                ImagePathAndProps.DEFEAT_MAIL_IMAGE_PATH.value
            )
            time_eclipsed = time.time() - start
            super().set_text(replace='Waiting: {}/{}'.format(int(time_eclipsed), self.bot.config.timeout), index=0)
            if found:
                super().set_text(insert='Victory' if name == VICTORY_MAIL else 'Defeat')
                return name
            elif time_eclipsed >= self.bot.config.timeout:
                super().set_text(insert='Timeout! Stop Task')
                return None

    def wait_for_commander_back_to_city(self, commander_cv_img):
        start = time.time()
        while True:
            result = self.gui.has_image_cv_img(commander_cv_img)
            time_eclipsed = time.time() - start
            super().set_text(
                replace='Wait Commander return to City: {}/{}'.format(int(time_eclipsed), self.bot.config.timeout),
                index=0)
            if result is None:
                return True
            elif time_eclipsed >= self.bot.config.timeout:
                super().set_text(insert='Timeout! Stop Task')
                return False

    def has_ap(self):
        name = self.gui.get_curr_gui_name()
        return True if name == WINDOW else False

    def use_ap_recovery(self):
        name, _ = self.gui.get_curr_gui_name()
        used = False
        if name == WINDOW:
            if self.bot.config.useDailyAPRecovery:
                _, _, pos = self.gui.check_any(ImagePathAndProps.DAILY_AP_CLAIM_BUTTON_IMAGE_PATH.value)
                if pos is not None:
                    super().set_text(insert='Use Daily AP Recovery')
                    super().tap(pos[0], pos[1], 1)
                    used = True
            if self.bot.config.useNormalAPRecovery and not used:
                _, _, pos = self.gui.check_any(ImagePathAndProps.USE_AP_BUTTON_IMAGE_PATH.value)
                if pos is not None:
                    super().set_text(insert='Use Normal AP Recovery')
                    for i in range(2):
                        super().tap(pos[0], pos[1], 1)
                    used = True
            if not used:
                super().set_text(insert='Run out of AP')
                raise RuntimeError('Run out of AP')
            super().back(3)
            return True

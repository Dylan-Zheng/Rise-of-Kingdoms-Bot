import traceback

from filepath.constants import MAP
from filepath.file_relative_paths import BuffsImageAndProps, ItemsImageAndProps, ImagePathAndProps
from tasks.Task import Task
from tasks.constants import TaskName, Resource
import time


class GatherGem(Task):

    def __init__(self, bot):
        super().__init__(bot)
        self.move_time = {
            "up": 0,
            "down": 0,
            "left": 0,
            "right" : 0
        }
        self.last_move = "up"

    def reset_move(self):
        self.move_time["up"] = 0
        self.move_time["down"] = 0
        self.move_time["left"] = 0
        self.move_time["right"] = 0

    # Function to decide what to move next, however it may missed some direction
    def get_next_move(self, allowed_time = 50):
        next_move = "done"
        if self.move_time["up"] >= allowed_time:
            if self.move_time["down"] >= allowed_time:
                if self.move_time["left"] >= allowed_time:
                    if self.move_time["right"] >= allowed_time:
                        self.reset_move()
                        return next_move
                    else:
                        next_move = "right"
                else:
                    next_move = "left"
            else:
                next_move = "down"
        else:
            next_move = "up"
        self.move_time[next_move] = self.move_time[next_move] + 1
        return next_move

    def do_move(self):
        next_move = self.get_next_move(self.bot.config.gatherGemDistance)
        if next_move == "done":
            self.last_move = "up"
            return False
        if next_move != self.last_move:
            self.back_to_home_gui()
            self.back_to_map_gui()
            self.last_move = next_move
        self.move(next_move)
        return True

    def do(self, next_task=TaskName.GATHER_GEM):
        magnifier_pos = (60, 540)
        self.set_text(title='Gather Gem', remove=True)
        # Start at any map location
        self.back_to_map_gui()
        last_resource_pos = []
        last_dir = "up"
        try:
            while True:
                # Check if gem mine exists on map
                found, _, gempost = self.gui.check_any(ImagePathAndProps.GEM_IMG_PATH.value)
                if found:
                    self.set_text(insert="Found gem pot")
                    # Tap on the gem mine
                    self.tap(gempost[0], gempost[1], 2)
                    new_resource_pos = self.gui.resource_location_image_to_string()
                    if new_resource_pos in last_resource_pos:
                        self.set_text(insert="Same node of gem")
                        # Same node, move the screen
                        if not self.do_move():
                            return next_task
                        continue
                    else:
                        # Save last node position, remember to reset the last resouse pos 
                        last_resource_pos.append(new_resource_pos)
                    # Check if we can gather the node
                    found, _, gather_button_pos = self.gui.check_any(ImagePathAndProps.RESOURCE_GATHER_BUTTON_IMAGE_PATH.value)
                    if found:
                        # Yes, send the troop
                        self.tap(gather_button_pos[0], gather_button_pos[1], 2)
                        pos = self.gui.check_any(ImagePathAndProps.NEW_TROOPS_BUTTON_IMAGE_PATH.value)[2]
                        if pos is None:
                            self.set_text(insert="Not more space for march")
                            return next_task
                        new_troops_button_pos = pos
                        self.tap(new_troops_button_pos[0], new_troops_button_pos[1], 2)
                        if True: #self.bot.config.gatherResourceNoSecondaryCommander:
                            self.set_text(insert="Remove secondary commander")
                            self.tap(473, 501, 0.5)
                        # Send match
                        match_button_pos = self.gui.check_any(ImagePathAndProps.TROOPS_MATCH_BUTTON_IMAGE_PATH.value)[2]
                        self.set_text(insert="March")
                        self.tap(match_button_pos[0], match_button_pos[1], 2)
                    else:
                        # Can't gather it, maybe farmed by anyone else
                        self.set_text(insert="Not farmable")
                        # Try to move screen
                        if not self.do_move():
                            return next_task
                        continue
                else:
                    if not self.do_move():
                        return next_task
        except Exception as e:
            traceback.print_exc()
            return next_task
        return next_task

    def check_query_space(self):
        found, _, _ = self.gui.check_any(ImagePathAndProps.HAS_MATCH_QUERY_IMAGE_PATH.value)
        curr_q, max_q = self.gui.match_query_to_string()
        if curr_q is None:
            return self.max_query_space
        return max_q - curr_q

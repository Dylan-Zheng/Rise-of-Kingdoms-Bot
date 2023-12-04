from filepath.file_relative_paths import ImagePathAndProps
from tasks.Task import Task
from tasks.constants import TaskName


class SunsetCanyon(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.MYSTERY_MERCHANT.value):
        self.set_text(title='Sunset Canyon', remove=True)
        campaign_btn_pos = (830, 670)
        self.back_to_home_gui()
        self.menu_should_open(True)
        x, y = campaign_btn_pos
        self.tap(x, y, 1)

        found, _, pos = self.gui.check_any(ImagePathAndProps.SUNSET_CANYON_IMAGE_PATH.value)
        if not found:
            self.set_text(insert='Sunset Canyon not found', index=0)
            return next_task

        self.set_text(insert='Open Sunset Canyon')
        x, y = pos
        self.tap(x, y, 1)

        while True:
            self.tap(640, 650, 1)
            free_attempts, ticket_attempts = self.gui.sunset_canyon_attempts_image_to_string()
            self.set_text(insert=f'Free attempts [{free_attempts}]. Ticket attempts [{ticket_attempts}]')
            if free_attempts == 0 and ticket_attempts == 0:
                self.set_text(insert='No more attempts left')
                break
            else:
                # Either we have attempts left, or we couldn't read the number of attempts
                # Try to challenge anyway and see if it works
                self.tap(950, 250, 6)
                # Verify that it opened and we can see the Ok button
                is_present, _, pos = self.gui.check_any(ImagePathAndProps.SUNSET_CANYON_OK_IMAGE_PATH.value)
                if not is_present:
                    self.set_text(insert='No more attempts left')
                    break

                # Check if skip battle button is checked, if not press it. Do this 3 times as there are sometimes
                # random clouds that go over the green check mark
                for i in range(0, 5):
                    is_checked, _, pos = self.gui.check_any(ImagePathAndProps.SKIP_BATTLE_CHECKED_IMAGE_PATH.value)
                    if is_checked:
                        break
                    # We did not find the check mark the first time, tap it and check again
                    self.tap(590, 590, 2)

                # Click OK
                self.tap(640, 650, 3)
                # Click again to go back
                self.tap(640, 650, 2)
                # Repeat

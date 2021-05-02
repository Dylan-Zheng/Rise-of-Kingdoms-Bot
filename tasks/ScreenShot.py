from tasks.Task import Task
from tasks.constants import TaskName


class ScreenShot(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do_city_screen(self):
        super().set_text(title='Get City Image', remove=True)
        super().set_text(append='Init Building Position', remove=True)
        super().set_text(append='init view')
        super().back_to_home_gui()
        super().home_gui_full_view()
        super().set_text(append='Done')
        return self.gui.get_curr_device_screen_img()

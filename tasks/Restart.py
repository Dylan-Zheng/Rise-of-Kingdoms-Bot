from tasks.Task import Task
from tasks.constants import TaskName


class Restart(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task = TaskName.BREAK ):
        super().set_text(title='Kill The Game', remove=True)
        super().set_text(insert='')
        super().stopRok()
        return next_task

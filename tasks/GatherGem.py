from filepath.file_relative_paths import ImagePathAndProps
from tasks.Task import Task
import traceback



class CourierStation(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.GATHER_GEM.value):
        print("none")
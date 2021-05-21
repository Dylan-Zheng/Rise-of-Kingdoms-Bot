from filepath.file_relative_paths import ImagePathAndProps
from tasks.Task import Task
import traceback

from tasks.constants import TaskName


class GatherGem(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.GATHER_GEM.value):
        print("none")
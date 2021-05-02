from tasks.Task import Task


from tasks.constants import TaskName


class ClaimVip(Task):
    def __init__(self, bot):
        super().__init__(bot)

    def do(self, next_task=TaskName.CLAIM_QUEST):
        vip_pos = (150, 65)
        vip_point_chest = (1010, 180)
        vip_free_chest = (920, 400)
        super().set_text(title='Claim VIP Chest', remove=True)
        super().back_to_home_gui()
        # tap on vip
        super().set_text(insert='Open VIP')
        x, y = vip_pos
        super().tap(x, y, 2)
        # tap on vip point chest
        super().set_text(insert='Claim daily vip point')
        x, y = vip_point_chest
        super().tap(x, y, 5)
        super().tap(x, y, 1)
        # tap on free chest
        super().set_text(insert='Claim daily free vip chest')
        x, y = vip_free_chest
        super().tap(x, y, 1)
        return next_task

from discord.ui import View
from config.config import INTEREST_ROLES
from components.buttons.interestButton import InterestButton

class InterestView(View):
    def __init__(self, active_role_ids: list[int]):
        super().__init__(timeout=None)
        for name, role_id in INTEREST_ROLES.items():
            self.add_item(InterestButton(label=name, role_id=role_id, active_role_ids=active_role_ids))
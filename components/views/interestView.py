import discord
from discord.ui import View
from config.config import INTEREST_ROLES
from components.buttons.interestButton import InterestButton

class InterestView(View):
    def __init__(self, active_role_id=None):
        super().__init__(timeout=None)
        for label, role_id in INTEREST_ROLES.items():
            style = discord.ButtonStyle.success if role_id == active_role_id else discord.ButtonStyle.primary
            self.add_item(InterestButton(label=label, role_id=role_id, active_role_id=active_role_id,style=style))
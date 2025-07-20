import discord
from discord.ui import View
from config.config import INTEREST_ROLES
from components.buttons.interestButton import InterestButton

class InterestView(discord.ui.View):
    def __init__(self, active_role_ids: list[int] = []):
        super().__init__(timeout=None)
        for label, role_id in INTEREST_ROLES.items():
            style = discord.ButtonStyle.success if role_id in active_role_ids else discord.ButtonStyle.primary
            self.add_item(InterestButton(label=label, role_id=role_id, style=style))
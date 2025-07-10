import discord
import json
from discord.ui import View
from components.buttons.verifyButton import verifyButton

class buttonHandler(View):
    def __init__(self, bot, title, description):
        super().__init__(timeout=None)
        self.bot = bot
        self.title = title
        self.description = description
        self.message_id = None
        self.add_item(verifyButton())

    async def send_embed(self,interaction):
        embed = discord.Embed(title=self.title, description= self.description, color=discord.Color.blue())
        await interaction.response.send_message(embed=embed,view=self)
        msg = await interaction.original_response()
        self.message_id = msg.id
        data = {
            "guild_id": msg.guild.id,
            "channel_id": msg.channel.id,
            "message_id": msg.id,
            "title": self.title,
            "description": self.description
        }
        with open("verify_message.json","w") as f:
            json.dump(data,f)



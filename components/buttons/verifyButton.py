import discord
from discord.ui import Button
from components.modals.verificationModal import verificationModal

class verifyButton(Button):
    def __init__(self):
        super().__init__(label="Verify", style=discord.ButtonStyle.success, custom_id="persistent_verify_button")
    
    async def callback(self, interaction: discord.Interaction):
        modal = verificationModal()
        await interaction.response.send_modal(modal)
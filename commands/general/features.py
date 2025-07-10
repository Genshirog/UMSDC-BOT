import discord
from config.config import ALLOWED_CHANNEL_ID
from components.views.interestView import InterestView

async def featuresCommand(bot, interaction):
    if interaction.channel.id != ALLOWED_CHANNEL_ID["Features"]:
        await interaction.response.send_message(
            "❌ This command can only be used in the designated features channel.",
            ephemeral=True
        )
        return
    embed = discord.Embed(
        title="🎯 Choose Your Interest",
        description="Select **one** interest below. Your previous interest will be removed.",
        color=discord.Color.orange()
    )
    await interaction.response.send_message(embed=embed, view=InterestView(), ephemeral=True)
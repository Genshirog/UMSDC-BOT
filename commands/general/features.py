import discord
from components.views.interestView import InterestView

async def featuresCommand(bot, interaction):
    embed = discord.Embed(
        title="🎯 Choose Your Interest",
        description="Select **one** interest below. Your previous interest will be removed.",
        color=discord.Color.orange()
    )
    await interaction.response.send_message(embed=embed, view=InterestView(), ephemeral=True)
import discord
from components.views.interestView import InterestView
from config.config import INTEREST_ROLES

async def featuresCommand(bot, interaction):
    # Collect the user's current interest roles
    active_roles = [r.id for r in interaction.user.roles if r.id in INTEREST_ROLES.values()]

    embed = discord.Embed(
        title="🎯 Choose Your Interest",
        description="Select **up to 3** interests below. Click again to remove.",
        color=discord.Color.orange()
    )

    await interaction.response.send_message(
        embed=embed,
        view=InterestView(active_role_ids=active_roles),
        ephemeral=True
    )

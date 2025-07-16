import discord
from config.config import UMSDC_CHANNEL_ID


async def welcome_handler(member: discord.Member):
    channel = member.guild.get_channel(UMSDC_CHANNEL_ID["Welcome"])
    if channel:
        await channel.send(f"Welcome to the server, {member.mention}! Be sure to check out the rules and verification yourself")
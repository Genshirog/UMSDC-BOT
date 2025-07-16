from utils.censorship import load_banned_words
import discord

async def censor_handler(message: discord.Message, bot: discord.Client):
    if message.author.bot:
        return
    
    banned_words = load_banned_words()
    content = message.content.lower()

    if any(word in content for word in banned_words):
        await message.delete()
        await message.channel.send(f"{message.author.mention}⚠️ Your message contained a banned word.", delete_after=5)
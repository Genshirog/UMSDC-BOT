import discord
from events.onReadyHandler import on_ready_handler
from discord.ext import commands
from config.config import TOKEN, VERIFY_EMBED, ALLOWED_CHANNEL_ID
from commands.general.features import featuresCommand
from commands.admin.verification import verification


intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    await on_ready_handler(bot)

    
@bot.tree.command(name="verifysetup", description="Send the verification embed.")
async def verifysetup(interaction: discord.Interaction):
    await verification(bot,interaction)

@bot.tree.command(name="features", description="Update your interest.")
async def features(interaction: discord.Interaction):
    await featuresCommand(bot,interaction)

bot.run(TOKEN)

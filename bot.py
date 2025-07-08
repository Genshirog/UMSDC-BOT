import discord
import asyncio
from discord.ext import commands
from config import TOKEN, REACTION_ROLES, ROLE_EMBED
from reactionRole import reactionRole
TOKEN = 'MTM5MjA4ODIyMzgzMTk0OTQxMg.GzfSTs.CQhXsciq5AzGTAALR7L4X3FgRFzEFOMFZ6XXzM'  # Replace this with your bot token

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix='/', intents=intents)

role_handler = reactionRole(
    bot,
    emoji_role_map=REACTION_ROLES,
    title=ROLE_EMBED["title"],
    description=ROLE_EMBED["description"]
)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command()
@commands.has_permissions(administrator = True)
async def setup_roles(ctx):
    await role_handler.send_embed(ctx)

@bot.event
async def on_raw_reaction_add(payload):
    await role_handler.handle_add(payload)

@bot.event
async def on_raw_reaction_remove(payload):
    await role_handler.handle_remove(payload)

bot.run(TOKEN)

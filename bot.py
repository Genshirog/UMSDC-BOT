import discord
import json
from discord.ext import commands
from config import TOKEN, VERIFY_EMBED
from featuresHandler import InterestView
from buttonHandler import buttonHandler

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()
    try:
        with open("verify_message.json","r") as f:
            data = json.load(f)
        guild = bot.get_guild(data["guild_id"])
        channel = bot.get_channel(data["channel_id"])
        message = await channel.fetch_message(data["message_id"])
        view = buttonHandler(bot, title=data["title"], description=data["description"])
        bot.add_view(view)
        await message.edit(view=view)
    except Exception as e:
        print(f"❌ Could not restore verification message: {e}")


@bot.tree.command(name="verifysetup", description="Send the verification embed.")
async def verifysetup(interaction: discord.Interaction):
    verify = buttonHandler(
    bot,
    title=VERIFY_EMBED["title"],
    description=VERIFY_EMBED["description"]
    )
    await verify.send_embed(interaction)

@bot.tree.command(name="features", description="Update your interest.")
async def features(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎯 Choose Your Interest",
        description="Select **one** interest below. Your previous interest will be removed.",
        color=discord.Color.orange()
    )
    await interaction.response.send_message(embed=embed, view=InterestView(), ephemeral=True)

bot.run(TOKEN)

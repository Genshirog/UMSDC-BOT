import discord
import json
from components.views.verificationView import buttonHandler

async def on_ready_handler(bot: discord.Client):
    print(f'Logged in as {bot.user}')
    guild = discord.Object(id=1392045881695408158)
    #bot.tree.clear_commands(guild=guild)
    await bot.tree.sync(guild=guild)
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
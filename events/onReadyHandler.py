import discord
import json
from components.views.verificationView import buttonHandler

async def on_ready_handler(bot: discord.Client):
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
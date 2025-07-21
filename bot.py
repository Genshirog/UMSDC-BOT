import discord
from events.onReadyHandler import on_ready_handler
from discord.ext import commands
from config.config import TOKEN, VERIFY_EMBED, ALLOWED_CHANNEL_ID
from commands.general.features import featuresCommand
from commands.admin.verification import verification
from events.on_message_censor import censor_handler
from events.on_members_join import welcome_handler
import webserver


intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True
intents.reactions = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=intents)

    async def setup_hook(self):
        await self.load_extension("commands.admin.censorGroup")
        await self.load_extension("commands.admin.purge")
        print("✅ Loaded command extensions.")

    async def on_ready(self):
        await on_ready_handler(self)

    async def on_message(self, message: discord.Message):
        await censor_handler(message=message, bot=self)
        await self.process_commands(message)

    async def on_member_join(self, member: discord.Member):
        await welcome_handler(member)

bot = MyBot()
    
# @bot.tree.command(name="verifysetup", description="Send the verification embed.")
# async def verifysetup(interaction: discord.Interaction):
#     if not interaction.user.guild_permissions.administrator:
#         await interaction.response.send_message(
#             "❌ You do not have permission to use this command.", ephemeral=True
#         )
#         return
#     await verification(bot,interaction)

@bot.tree.command(name="features", description="Update your interest.")
async def features(interaction: discord.Interaction):
    await featuresCommand(bot,interaction)

#webserver.keep_alive()
bot.run(TOKEN)

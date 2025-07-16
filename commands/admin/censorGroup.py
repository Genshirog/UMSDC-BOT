import discord
from discord.ext import commands
from discord import app_commands
from utils.censorship import load_banned_words, save_banned_words

class CensorGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="censor", description="Manage censored words")

    @app_commands.command(name="add", description="Add a new censored word")
    async def add_word(self, interaction: discord.Interaction, word: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You do not have permission to use this command.", ephemeral=True
            )
            return
        word = word.lower()
        banned = load_banned_words()
        if word in banned:
            await interaction.response.send_message("❗ Word is already censored.", ephemeral=True)
        else:
            banned.append(word)
            save_banned_words(banned)
            await interaction.response.send_message(f"✅ Added `{word}` to banned words.", ephemeral=True)

    @app_commands.command(name="remove", description="Remove a censored word")
    async def remove_word(self, interaction: discord.Interaction, word: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You do not have permission to use this command.", ephemeral=True
            )
            return
        word = word.lower()
        banned = load_banned_words()
        if word not in banned:
            await interaction.response.send_message("❌ Word not found in the list.", ephemeral=True)
        else:
            banned.remove(word)
            save_banned_words(banned)
            await interaction.response.send_message(f"🗑 Removed `{word}` from banned words.", ephemeral=True)

    @app_commands.command(name="list", description="List all censored words")
    async def list_words(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ You do not have permission to use this command.", ephemeral=True
            )
            return
        banned = load_banned_words()
        if not banned:
            await interaction.response.send_message("✅ No banned words yet.", ephemeral=True)
        else:
            word_list = ", ".join(f"`{w}`" for w in banned)
            await interaction.response.send_message(f"🚫 **Censored Words:**\n{word_list}", ephemeral=True)

# Register it as a cog
class CensorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(CensorGroup())

async def setup(bot):
    await bot.add_cog(CensorCog(bot))

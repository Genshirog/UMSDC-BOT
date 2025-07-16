import discord
from discord import app_commands
from discord.ext import commands

class Purge(commands.Cog):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
    
    @commands.hybrid_command(name="purge", description="Delete a number of messages in the current channel.")
    @commands.has_permissions(manage_messages=True)
    async def purgeCommand(self, ctx: commands.Context,amount: int):
        if amount < 1 or amount > 100:
            await ctx.send(
                "⚠️ Please specify a number between 1 and 100.",
                ephemeral=True
            )
            return
        await ctx.channel.purge(limit=amount)

async def setup(bot):
    await bot.add_cog(Purge(bot))
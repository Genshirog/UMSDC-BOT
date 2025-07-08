import discord
from discord.ext import commands
import asyncio

class reactionRole:
    def __init__(self, bot, emoji_role_map, title, description):
        self.bot = bot;
        self.emoji_role_map = emoji_role_map;
        self.title = title;
        self.description = description;
        self.message_id = None;
    
    async def send_embed(self,ctx):
        embed = discord.Embed(title=self.title, description=self.description, color=discord.Color.blue())
        msg = await ctx.send(embed=embed)
        self.message_id = msg.id
        for emoji in self.emoji_role_map:
            await msg.add_reaction(emoji)

    async def handle_add(self, payload):
        if payload.user_id == self.bot.user.id or payload.message_id != self.message_id:
            return
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        emoji = str(payload.emoji)

        if emoji not in self.emoji_role_map:
            return
        
        role_name = self.emoji_role_map[emoji]
        role = discord.utils.get(guild.roles, name=role_name)
        channel = self.bot.get_channel(payload.channel_id)
        message = discord.PartialMessage(channel=channel, id=payload.message_id)

        tasks = []

        for e, r_name in self.emoji_role_map.items():
            if e != emoji:
                other_role = discord.utils.get(guild.roles, name=r_name)
                tasks.append(member.remove_roles(other_role))
                tasks.append(member.remove_reaction(e,discord.Object(id=payload.user_id)))
        tasks.append(member.add_roles(role))
        await asyncio.gather(*tasks)
    
    async def handle_remove(self,payload):
        if payload.message_id != self.message_id:
            return
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        emoji = str(payload.emoji)

        if emoji not in self.emoji_role_map:
            return
        role_name = self.emoji_role_map[emoji]
        role = discord.utils.get(guild.role, name=role_name)
        if role and member and role in member.role:
            await member.remove_roles(role)
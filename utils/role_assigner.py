import discord

async def assign_roles(interaction, course, status):
        guild = interaction.guild
        if isinstance(course,int):
            role_course = guild.get_role(course)
        else:
            role_course = discord.utils.get(guild.roles, name=course)

        if isinstance(status, int):
            role_status = guild.get_role(status)
        else:
            role_status = discord.utils.get(guild.roles, name=status)

        # Assign roles
        if role_course:
            await interaction.user.add_roles(role_course)
        else:
            print(f"⚠️ Course role '{course}' not found.")
            
        if role_status:
            await interaction.user.add_roles(role_status)
        else:
            print(f"⚠️ Status role '{status}' not found.")
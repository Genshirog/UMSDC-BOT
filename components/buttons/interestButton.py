import discord
from discord.ui import Button
from config.config import INTEREST_ROLES
from database.dbConnection import get_db_connector

class InterestButton(Button):
    def __init__(self, label: str, role_id: int, active_role_id: int = None,style=discord.ButtonStyle.primary):
        super().__init__(label=label, style=style, custom_id=f"interest_{role_id}")
        self.role_id = role_id
        self.disabled = (role_id == active_role_id)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user

        # Remove all existing interest roles
        to_remove = [guild.get_role(rid) for rid in INTEREST_ROLES.values() if rid in [r.id for r in member.roles]]
        await member.remove_roles(*[r for r in to_remove if r])
        
        # Add the selected interest role
        selected_role = guild.get_role(self.role_id)
        if selected_role:
            await member.add_roles(selected_role)

            # Send a new view with updated button highlight
            from components.views.interestView import InterestView  # ✅ local import
            new_view = InterestView(active_role_id=self.role_id)
            
            await interaction.response.edit_message(content=f"✅ You’ve selected **{selected_role.name}**.", view=new_view)
        else:
            await interaction.response.send_message("❌ Role not found.", ephemeral=True)

        # Inside your InterestButton.callback
        conn = get_db_connector()
        cursor = conn.cursor()

        # Update interest for the user
        cursor.execute("UPDATE users SET interest = %s WHERE discord_id = %s", (self.role_id, interaction.user.id))
        conn.commit()
        conn.close()

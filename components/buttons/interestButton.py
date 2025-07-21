import discord
from discord.ui import Button
from config.config import INTEREST_ROLES
from database.dbConnection import get_db_connector

MAX_INTEREST_ROLES = 3  # Maximum number of interest roles allowed

class InterestButton(Button):
    def __init__(self, label: str, role_id: int, active_role_ids: list[int], style_if_active=discord.ButtonStyle.success, style_if_inactive=discord.ButtonStyle.primary):
        style = style_if_active if role_id in active_role_ids else style_if_inactive
        super().__init__(label=label, style=style, custom_id=f"interest_{role_id}")
        self.role_id = role_id
        # self.disabled = (role_id == active_role_id)  # ⛔ Only relevant if single-role selection

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        selected_role = guild.get_role(self.role_id)

        if not selected_role:
            await interaction.response.send_message("❌ Role not found.", ephemeral=True)
            return

        current_interest_roles = [guild.get_role(rid) for rid in INTEREST_ROLES.values() if rid in [r.id for r in member.roles]]

        if selected_role in current_interest_roles:
            await member.remove_roles(selected_role)
            action = f"❎ Removed **{selected_role.name}**."
        else:
            if len(current_interest_roles) >= MAX_INTEREST_ROLES:
                await interaction.response.send_message(f"⚠️ You can only have **{MAX_INTEREST_ROLES}** interest roles.", ephemeral=True)
                return
            await member.add_roles(selected_role)
            action = f"✅ Added **{selected_role.name}**."

        # 🔄 Refresh member to get updated role list
        updated_member = await guild.fetch_member(member.id)
        active_role_ids = [r.id for r in updated_member.roles if r.id in INTEREST_ROLES.values()]

        from components.views.interestView import InterestView
        new_view = InterestView(active_role_ids=active_role_ids)

        await interaction.response.edit_message(content=action, view=new_view)


        # Database logic (optional: re-enable if needed)
        # conn = get_db_connector()
        # cursor = conn.cursor()

        # # You can store roles as a list or comma-separated string if your DB allows it
        # cursor.execute("UPDATE users SET interests = %s WHERE discord_id = %s", (",".join(str(r.id) for r in current_interest_roles), interaction.user.id))
        # conn.commit()
        # conn.close()

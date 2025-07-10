import discord
from discord.ui import Modal,TextInput
from database.dbConnection import get_db_connector
from utils.role_assigner import assign_roles

class verificationModal(Modal):
    def __init__(self):
        super().__init__(title="Verification Form")
        self.email = TextInput(label="Enter your umindanao email", placeholder="e.xample.123@umindanao.edu.ph", required=True)
        self.name = TextInput(label="Enter your fullname", placeholder="John Smith", required=True)
        self.course = TextInput(label="Enter your course", placeholder="IT,CS,CpE", required= True)
        self.add_item(self.email)
        self.add_item(self.name)
        self.add_item(self.course)

    async def on_submit(self, interaction: discord.Interaction):
        email_value = self.email.value.strip()
        course_input = self.course.value.strip().upper()
        name_value = self.name.value.strip()
        discord_id = interaction.user.id

        status_map = {
            "member": 1392046054702059581,
            "guest": 1392048440661250118
        }

        if email_value.endswith("@umindanao.edu.ph"):
            status_value = status_map["member"]
        else:
            status_value = status_map["guest"]
        
        course_map = {
            "IT": 1392058308067594321,
            "CS": 1392058450703286282,
            "CPE": 1392058533373153291
        }

        if status_value == status_map["member"]:
            course_value = course_map.get(course_input)
            if not course_value:
                await interaction.response.send_message(
                    "❌ Invalid course entered. Please use IT, CS, or CpE.",
                    ephemeral=True
                )
                return
        else:
            course_value = None
        
        try:
            conn = get_db_connector()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users(discord_id,email,fullname,status,courses) VALUES (%s,%s,%s,%s,%s)',(discord_id,email_value,name_value,status_value,course_value))
            conn.commit()
            conn.close()

            await assign_roles(interaction,course_value,status_value)
            await interaction.response.send_message("✅ Verification successful! You've been assigned your roles.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

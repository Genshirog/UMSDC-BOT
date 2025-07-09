import discord
import dbConnection
import json
from discord.ui import View, Button,Modal,TextInput

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

        course_value = course_map.get(course_input)

        if not course_value:
            await interaction.response.send_message(
                "❌ Invalid course entered. Please use IT, CS, or CpE.",
                ephemeral=True
            )
            return
        
        try:
            conn = dbConnection.get_db_connector()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users(discord_id,email,fullname,status,courses) VALUES (%s,%s,%s,%s,%s)',(discord_id,email_value,name_value,status_value,course_value))
            conn.commit()
            conn.close()

            await assign_roles(interaction,course_value,status_value)
            await interaction.response.send_message("✅ Verification successful! You've been assigned your roles.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

class verifyButton(Button):
    def __init__(self):
        super().__init__(label="Verify", style=discord.ButtonStyle.success, custom_id="persistent_verify_button")
    
    async def callback(self, interaction: discord.Interaction):
        modal = verificationModal()
        await interaction.response.send_modal(modal)

class buttonHandler(View):
    def __init__(self, bot, title, description):
        super().__init__(timeout=None)
        self.bot = bot
        self.title = title
        self.description = description
        self.message_id = None
        self.add_item(verifyButton())

    async def send_embed(self,interaction):
        embed = discord.Embed(title=self.title, description= self.description, color=discord.Color.blue())
        await interaction.response.send_message(embed=embed,view=self)
        msg = await interaction.original_response()
        self.message_id = msg.id
        data = {
            "guild_id": msg.guild.id,
            "channel_id": msg.channel.id,
            "message_id": msg.id,
            "title": self.title,
            "description": self.description
        }
        with open("verify_message.json","w") as f:
            json.dump(data,f)


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
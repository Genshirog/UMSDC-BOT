import discord
from config.config import ALLOWED_CHANNEL_ID,VERIFY_EMBED
from components.views.verificationView import buttonHandler

async def verification(bot,interaction):
    if interaction.channel.id != ALLOWED_CHANNEL_ID["Verify"]:
        await interaction.response.send_message(
            "❌ This command can only be used in the designated verification setup channel.",
            ephemeral=True
        )
        return
    verify = buttonHandler(
    bot,
    title=VERIFY_EMBED["title"],
    description=VERIFY_EMBED["description"]
    )
    await verify.send_embed(interaction)
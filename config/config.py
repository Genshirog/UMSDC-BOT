import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

VERIFY_EMBED = {
    "title": "Verification Form",
    "description": "Click on the button to open up the form"
}

INTEREST_ROLES = {
    "Programming":1392083215392571402,
    "Cybersecurity": 1392083280249098323,
    "UI/UX":1392083388021608549,
    "Robotics":1392083434179923978
}

ALLOWED_CHANNEL_ID = {
    "Verify":1392056127230967889,
    "Features":1392374540704940152
}
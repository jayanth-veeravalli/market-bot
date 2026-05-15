import os
from dotenv import load_dotenv

if os.path.exists(".env.local"):
    load_dotenv(".env.local")
else:
    load_dotenv()

from bot import bot

bot.run(os.environ["DISCORD_BOT_TOKEN"])

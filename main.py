from dotenv import load_dotenv
load_dotenv()

import os
from bot import bot

bot.run(os.environ["DISCORD_BOT_TOKEN"])

import os

import discord
from discord import app_commands

from commands.watchlist import watchlist_group
from commands.premiums import premiums_group


class Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        self.tree.add_command(watchlist_group)
        self.tree.add_command(premiums_group)

        @self.tree.command(name="help", description="Show available commands")
        async def help_cmd(interaction: discord.Interaction):
            msg = (
                "**Market Research Bot — Commands**\n\n"
                "`/watchlist fetch` — Show all stocks in the watchlist\n"
                "`/watchlist add [ticker]` — Add a stock to the watchlist\n"
                "`/watchlist remove [ticker]` — Remove a stock from the watchlist\n\n"
                "`/premiums fetch` — Fetch put premiums for all watchlist stocks\n"
                "`/premiums stock [ticker]` — Fetch put premiums for a specific ticker\n\n"
                "_Premiums shown for strikes 20–30% below current price, current & next week expiry._"
            )
            await interaction.response.send_message(msg)

    async def on_ready(self):
        if os.environ.get("ENV") == "local":
            guild = discord.Object(id=int(os.environ["DISCORD_GUILD_ID"]))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()
        print(f"✅ Logged in as {self.user} — slash commands synced.")


bot = Bot()

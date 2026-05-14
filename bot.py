import discord
from discord.ext import commands

from commands.watchlist import watchlist_group
from commands.premiums import premiums_group

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

bot.tree.add_command(watchlist_group)
bot.tree.add_command(premiums_group)


@bot.tree.command(name="help", description="Show available commands")
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


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user} — slash commands synced.")

import discord
from discord import app_commands

import services.watchlist as watchlist_service

watchlist_group = app_commands.Group(
    name="watchlist",
    description="Manage your stock watchlist",
)


@watchlist_group.command(name="fetch", description="Show all stocks in the watchlist")
async def watchlist_fetch(interaction: discord.Interaction):
    await interaction.response.send_message(await watchlist_service.fetch_all())


@watchlist_group.command(name="add", description="Add a stock to the watchlist")
@app_commands.describe(ticker="Stock ticker symbol e.g. AAPL")
async def watchlist_add(interaction: discord.Interaction, ticker: str):
    await interaction.response.send_message(await watchlist_service.add_ticker(ticker))


@watchlist_group.command(name="remove", description="Remove a stock from the watchlist")
@app_commands.describe(ticker="Stock ticker symbol to remove")
async def watchlist_remove(interaction: discord.Interaction, ticker: str):
    await interaction.response.send_message(await watchlist_service.remove_ticker(ticker))

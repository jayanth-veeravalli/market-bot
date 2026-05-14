import discord
from discord import app_commands

import services.watchlist as watchlist_service
from services.alpaca import fetch_puts_for_ticker
from services.formatter import format_result

premiums_group = app_commands.Group(
    name="premiums",
    description="Check sell put premiums",
)


async def _send_result(interaction: discord.Interaction, ticker: str):
    result = fetch_puts_for_ticker(ticker)
    for msg in format_result(result):
        await interaction.followup.send(msg)


@premiums_group.command(name="fetch", description="Fetch put premiums for all watchlist stocks")
async def premiums_fetch(interaction: discord.Interaction):
    await interaction.response.defer()
    tickers = await watchlist_service.get_tickers()
    if not tickers:
        await interaction.followup.send("Your watchlist is empty. Use `/watchlist add` first.")
        return

    for ticker in tickers:
        await _send_result(interaction, ticker)


@premiums_group.command(name="stock", description="Fetch put premiums for a specific ticker")
@app_commands.describe(ticker="Stock ticker symbol e.g. AAPL")
async def premiums_stock(interaction: discord.Interaction, ticker: str):
    await interaction.response.defer()
    await _send_result(interaction, ticker)

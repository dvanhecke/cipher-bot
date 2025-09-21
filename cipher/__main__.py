# Cipher-Bot
# Copyright (c) 2025 dvanhecke
# Licensed under the MIT License

"""
Module: cipher
Main entry point for the Cipher-Bot minigames Discord bot.

Responsibilities:
- Initialize the Discord bot instance
- Load all minigame cogs/extensions
- Handle bot events and commands
- Start the bot event loop
"""

import os
import asyncio

import discord
from discord.ext import commands


TOKEN = os.getenv("BOT_TOKEN")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")

COGS = [
    "cipher.cogs.hangman",
    "cipher.cogs.number_guessing",
    "cipher.cogs.rockpaperscissors",
]


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)
tree = client.tree


@client.event
async def on_ready():
    """
    Function to run when getting the bot ready
    - syncs the application command tree
    """
    synced = await tree.sync()
    print(f"Synced {len(synced)} commands globally")
    print(f"{client.user} has connected to Discord!")


@client.hybrid_command(name="help", description="Show the help menu")
async def hybrid_help(ctx):
    """
    help command for the bot
    """
    embed = discord.Embed(title="📖 Help Menu", color=discord.Color.gold())
    for command in client.commands:
        if command.hidden:
            continue
        embed.add_field(
            name=f"{COMMAND_PREFIX}{command.name} /{command.name}",
            value=command.description or "No description provided.",
            inline=False,
        )
    if not ctx.interaction:
        await ctx.message.delete()
        await ctx.send(embed=embed, delete_after=10)
    else:
        await ctx.interaction.response.send_message(embed=embed, ephemeral=True)


@client.command(hidden=True)
@commands.is_owner()
async def ping(ctx):
    """
    bot owner only command to test latency of the bot
    """
    await ctx.message.delete()
    await ctx.send(f"Pong! Latency: {round(ctx.bot.latency * 1000)}ms", delete_after=5)


async def load_cogs(bot):
    """Load all cogs asynchronously."""
    for cog in COGS:
        await bot.load_extension(cog)
        print(f"Loaded {cog}")


if __name__ == "__main__":

    async def main():
        """main function to start the bot"""
        await load_cogs(client)
        try:
            await asyncio.shield(client.start(TOKEN))
        except KeyboardInterrupt:
            print("KeyboardInterrupt received. Shutting down...")
        finally:
            await client.close()

    asyncio.run(main())

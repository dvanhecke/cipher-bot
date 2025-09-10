import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cipher.rockpaperscissors import RockPaperScissors
from cipher.guessnumber import (
    start_guessing_game,
    get_guessing_state,
    handle_guessing_guess,
)
from cipher.hangman import (
    start_hangman_game,
    get_hangman_state,
    handle_hangman_guess,
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents, help_command=None)
tree = client.tree


@client.event
async def on_ready():
    synced = await tree.sync()
    print(f"Synced {len(synced)} commands globally")
    print(f"{client.user} has connected to Discord!")


@client.hybrid_command(name="help", description="Show the help menu")
async def hybrid_help(ctx):
    embed = discord.Embed(title="📖 Help Menu", color=discord.Color.gold())
    for command in client.commands:
        if command.hidden:
            continue
        embed.add_field(
            name=f"!{command.name} /{command.name}",
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
    await ctx.message.delete()
    await ctx.send(f"Pong! Latency: {round(ctx.bot.latency * 1000)}ms", delete_after=5)


@client.hybrid_command(
    name="rps", description="Play rock paper scissors against the bot"
)
async def rps(ctx, *, choice: RockPaperScissors()):
    await ctx.send(choice)


@client.hybrid_command(
    name="guess",
    description="to start don't add a number otherwise guess the number between 0 and 100",
)
async def guess(ctx, number=None):
    if not ctx.interaction:
        await ctx.message.delete()
    if number is None:
        await start_guessing_game(ctx)
        return

    state = get_guessing_state(ctx)
    if not state:
        await ctx.send("No active game here! Start with `!guess`.", delete_after=5)
        return

    await ctx.send("Parsing the guess", delete_after=1)
    await handle_guessing_guess(ctx, state, number)


@client.hybrid_command(
    name="hangman",
    description="Let's play hangman to start don't add a letter otherwise guess the word",
)
async def hangman(ctx, letter=None):
    if not ctx.interaction:
        await ctx.message.delete()

    if letter is None:
        await start_hangman_game(ctx)
        return

    state = get_hangman_state(ctx)
    if not state:
        await ctx.send("No active game here! Start with `!hangman`.", delete_after=5)
        return

    await ctx.send("Parsing the guess", delete_after=1)
    await handle_hangman_guess(ctx, state, letter)


if __name__ == "__main__":
    client.run(TOKEN)

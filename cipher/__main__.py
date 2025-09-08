import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cipher.rockpaperscissors import RockPaperScissors
from cipher.guessnumber import GuessNumber
from cipher.hangman import start_hangman_game, get_hangman_state, handle_hangman_guess

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


@client.command()
async def ping(ctx):
    await ctx.send("Pong")


@client.command()
async def rps(ctx, *, win: RockPaperScissors()):
    await ctx.send(win)


@client.command()
async def guess(ctx, *, win: GuessNumber()):
    await ctx.send(win)


@client.command()
async def hangman(ctx, letter=None):
    await ctx.message.delete()

    if letter is None:
        await start_hangman_game(ctx)
        return

    state = get_hangman_state(ctx)
    if not state:
        await ctx.send("No active game here! Start with `!hangman`.", delete_after=5)
        return

    await handle_hangman_guess(ctx, state, letter)


if __name__ == "__main__":
    client.run(TOKEN)

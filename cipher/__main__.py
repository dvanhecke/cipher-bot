import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cipher.rockpaperscissors import RockPaperScissors
from cipher.guessnumber import GuessNumber
from cipher.hangman import *

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
    if ctx.channel.id in hangman_games and letter is None:
        await ctx.send("Game already running!")
        return

    if letter is None:
        word = random.choice(HANGMAN_WORDS)
        display = ["_" for _ in word]
        hangman_games[ctx.channel.id] = {
            "word": word,
            "display": display,
            "wrong": [],
        }
        await ctx.send(f"Let's play Hangman!\n```{HANGMAN_PICS[0]}```\nWord: ```{' '.join(display)}```")
        return
    state = hangman_games.get(ctx.channel.id)
    if not state:
        await ctx.send("No active game here! Start with `!hangman`.")
        return
    letter = letter.lower()
    if letter in state["display"] or letter in state["wrong"]:
        await ctx.send("You already guessed that!")
        return

    if letter in state["word"]:
        for i, ch in enumerate(state["word"]):
            if ch == letter:
                state["display"][i] = letter
        if letter == state["word"]:
            for i, ch in enumerate(state["word"]):
                state["display"][i] = ch
    else:
        state["wrong"].append(letter)

    stage = len(state["wrong"])
    await ctx.send(
        f"```{HANGMAN_PICS[stage]}```\nWord: ```{' '.join(state['display'])}```\nWrong: {', '.join(state['wrong'])}"
    )

    if "_" not in state["display"]:
        await ctx.send(f"🎉 You guessed it! The word was **{state['word']}**.")
        del hangman_games[ctx.channel.id]
    elif stage >= len(HANGMAN_PICS) - 1:
        await ctx.send(f"💀 You lost! The word was **{state['word']}**.")
        del hangman_games[ctx.channel.id]


if __name__ == "__main__":
    client.run(TOKEN)

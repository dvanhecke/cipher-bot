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


def build_embed(state):
    stage = len(state["wrong"])
    embed = discord.Embed(
        title="🔠 Hangman",
        description=f"```{HANGMAN_PICS[stage]}```",
        color=0xffc300 if stage < len(HANGMAN_PICS) - 1 else 0xff0000
    )
    embed.add_field(name="Word", value=f"```{" ".join(state["display"])}```", inline=False)
    embed.add_field(name="Wrong guesses", value=", ".join(state["wrong"]) or "None", inline=False)
    return embed


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
    if ctx.channel.id in hangman_games and letter is None:
        await ctx.send("Game already running!", delete_after=5)
        return

    if letter is None:
        word = random.choice(HANGMAN_WORDS)
        display = ["_" for _ in word]
        hangman_games[ctx.channel.id] = {
            "word": word,
            "display": display,
            "wrong": [],
        }
        embed = build_embed(hangman_games[ctx.channel.id])
        msg = await ctx.send(embed=embed)
        hangman_games[ctx.channel.id]["message"] = msg
        return
    state = hangman_games.get(ctx.channel.id)
    if not state:
        await ctx.send("No active game here! Start with `!hangman`.", delete_after=5)
        return
    letter = letter.lower()
    if letter in state["display"] or letter in state["wrong"]:
        await ctx.send("You already guessed that!", delete_after=5)
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
    embed = build_embed(state)
    await state["message"].edit(embed=embed)

    stage = len(state["wrong"])

    if "_" not in state["display"]:
        embed.add_field(name="🏆 Solved by", value=ctx.author.display_name, inline=False)
        await state["message"].edit(embed=embed)
        await ctx.send(f"🎉 You guessed it! The word was **{state['word']}**. Solved by {ctx.author.mention}", delete_after=5)
        del hangman_games[ctx.channel.id]
    elif stage >= len(HANGMAN_PICS) - 1:
        for i, ch in enumerate(state["word"]):
            state["display"][i] = ch
        embed.add_field(name="💀 Hanged", value=ctx.author.display_name, inline=False)
        await state["message"].edit(embed=embed)
        await ctx.send(f"💀 You lost! The word was **{state['word']}**.", delete_after=5)
        del hangman_games[ctx.channel.id]


if __name__ == "__main__":
    client.run(TOKEN)

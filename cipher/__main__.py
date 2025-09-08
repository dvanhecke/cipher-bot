import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cipher.rockpaperscissors import RockPaperScissors

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
    print(f"user: {ctx.author}, has used ping command")
    await ctx.send("Pong")


@client.command()
async def rps(ctx, *, win: RockPaperScissors()):
    await ctx.send(win)


if __name__ == "__main__":
    client.run(TOKEN)

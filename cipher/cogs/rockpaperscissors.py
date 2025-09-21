# Cipher-Bot Rock paper scissors Cog
# Copyright (c) 2025 dvanhecke
# Licensed under the MIT License

"""
Rock paper scissors minigame cog for Cipher-Bot.
Handles processing games through Discord commands.
"""

from discord.ext import commands
import discord
from cipher.logic.rockpaperscissors import play_game
from cipher.utils.functions import build_embed


class RockPaperScissors(commands.Cog):
    """Cog for the rock paper scissors game."""

    def __init__(self, bot):
        """
        Initialize RockPaperScissors Cog

        Args:
            bot (commands.Bot): Discord bot instance
        """
        self.bot = bot

    @commands.hybrid_command(
        name="rps",
        description="Play rock paper scissors against me",
    )
    async def rps(self, ctx, choice: str):
        """
        Plays a game of rock paper scissors against the bot

        Args:
            ctx: discord.py Context
            choice (str): User's choice to play rock, paper or scissors
        """

        if not ctx.interaction:
            await ctx.message.delete()

        try:
            result = play_game(choice)
        except ValueError as e:
            await ctx.send(e, delete_after=10)
            return
        embed = build_embed("🪨📄✂️ Rock-Paper-Scissors", discord.Color.blue(), result)
        await ctx.send(embed=embed)


async def setup(bot):
    """
    Setup function for this cog.

    Args:
        bot (commands.Bot): Discord bot instance
    """
    await bot.add_cog(RockPaperScissors(bot))

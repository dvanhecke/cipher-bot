# Cipher-Bot Hangman Cog
# Copyright (c) 2025 dvanhecke
# Licensed under the MIT License

"""
Hangman minigame cog for Cipher-Bot.
Handles starting games and processing guesses through Discord commands.
"""

from discord.ext import commands
from cipher.utils.hangman import (
    start_game,
    get_state,
    handle_guess,
)


class Hangman(commands.Cog):
    """Cog for the Hangman minigame."""

    def __init__(self, bot):
        """
        Initialize Hangman Cog.

        Args:
            bot (commands.Bot): Discord bot instance
        """
        self.bot = bot

    @commands.hybrid_command(
        name="hangman",
        description="Play hangman. Start without a letter, guess by providing a letter or word.",
    )
    async def hangman(self, ctx, letter: str = None):
        """
        Start a new hangman game or guess a letter/word.

        Args:
            ctx: discord.py Context
            letter (str, optional): Letter or word to guess. Defaults to None.
        """
        if not ctx.interaction:
            await ctx.message.delete()

        if letter is None:
            await start_game(ctx)
            return

        state = get_state(ctx)
        if not state:
            await ctx.send(
                "No active game here! Start a new game with `!hangman`.", delete_after=5
            )
            return

        await ctx.send("Parsing your guess...", delete_after=1)
        await handle_guess(ctx, state, letter)


async def setup(bot):
    """
    Setup function for this cog.

    Args:
        bot (commands.Bot): Discord bot instance
    """
    await bot.add_cog(Hangman(bot))

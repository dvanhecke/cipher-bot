# Cipher-Bot Number guessing Cog
# Copyright (c) 2025 dvanhecke
# Licensed under the MIT License

"""
Number guessing minigame cog for Cipher-Bot.
Handles starting games and processing guesses through Discord commands.
"""

from discord.ext import commands
from cipher.utils.number_guessing import (
    start_game,
    get_state,
    handle_guess,
)


class Guess(commands.Cog):
    """Cog for the number guessing minigame."""

    def __init__(self, bot):
        """
        Initialize number guessing Cog.

        Args:
            bot (commands.Bot): Discord bot instance
        """
        self.bot = bot

    @commands.hybrid_command(
        name="guess",
        description="to start don't add a number otherwise guess the number between 0 and 100",
    )
    async def guess(self, ctx, number=None):
        """
        Start a new guessing game or guess a number.

        Args:
            ctx: discord.py Context
            number (int, optional): Number to guess. Defaults to None.
        """
        if not ctx.interaction:
            await ctx.message.delete()
        if number is None:
            await start_game(ctx)
            return

        state = get_state(ctx)
        if not state:
            await ctx.send("No active game here! Start with `!guess`.", delete_after=5)
            return

        await ctx.send("Parsing the guess", delete_after=1)
        await handle_guess(ctx, state, number)


async def setup(bot):
    """
    Setup function for this cog.

    Args:
        bot (commands.Bot): Discord bot instance
    """
    await bot.add_cog(Guess(bot))

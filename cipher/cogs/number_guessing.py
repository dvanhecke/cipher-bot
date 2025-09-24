# Cipher-Bot Number guessing Cog
# Copyright (c) 2025 dvanhecke
# Licensed under the MIT License

"""
Number guessing minigame cog for Cipher-Bot.
Handles starting games and processing guesses through Discord commands.
"""

from typing import Optional, Tuple, Dict
import os

from discord.ext import commands
import discord
from cipher.logic.number_guessing import NumberGuessing
from cipher.utils.functions import build_embed


class Guess(commands.Cog):
    """Cog for the number guessing minigame."""

    def __init__(self, bot):
        """
        Initialize number guessing Cog.

        Args:
            bot (commands.Bot): Discord bot instance
        """
        self.bot = bot
        self.active_games: Dict[
            int, Tuple[NumberGuessing, Optional[discord.Message]]
        ] = {}
        self.max_number = int(os.getenv("GUESSING_GAME_MAX_NUMBER", "100"))

    @commands.hybrid_command(
        name="guess",
        description=f"guess the number between 0 and {os.getenv(
            'GUESSING_GAME_MAX_NUMBER', '100'
            )}",
    )
    async def guess(self, ctx, guess: int):
        """
        Start a new guessing game or guess a number.

        Args:
            ctx: discord.py Context
            number (int): Number to guess.
        """
        if not ctx.interaction:
            await ctx.message.delete()
        else:
            await ctx.send("parsing your guess", delete_after=1)

        if ctx.channel.id not in self.active_games:
            self.active_games[ctx.channel.id] = (NumberGuessing(self.max_number), None)

        game: NumberGuessing = self.active_games[ctx.channel.id][0]
        msg = self.active_games[ctx.channel.id][1]

        try:
            game.play(guess)
        except ValueError as e:
            await ctx.send(f"Error: {e}", delete_after=5)
            return

        embed_data = game.embed_message_data
        embed = build_embed(
            title="Number Guessing Game",
            description="Try to guess the correct number!",
            color=discord.Color.blurple(),
            fields=embed_data,
        )

        if ctx.interaction:  # Slash command
            if not msg:  # first response
                msg = await ctx.send(embed=embed)
                self.active_games[ctx.channel.id] = (game, msg)
            else:
                await msg.edit(embed=embed)
        else:  # Prefix command
            if not msg:
                msg = await ctx.send(embed=embed)
                self.active_games[ctx.channel.id] = (game, msg)
            else:
                await msg.edit(embed=embed)

        # Announce result
        if game.result == "correct":
            await ctx.send(
                f"🎉 Correct! The number was {guess}. Game over.", delete_after=5
            )
            game.is_active = False
            del self.active_games[ctx.channel.id]


async def setup(bot):
    """
    Setup function for this cog.

    Args:
        bot (commands.Bot): Discord bot instance
    """
    await bot.add_cog(Guess(bot))

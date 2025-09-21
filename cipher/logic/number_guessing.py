# Cipher-Bot number guessing logic
# Copyright (c) 2025 dvanhecke
# Licensed under the MIT License

"""
Logic for numberguessing minigame.
Contains game state management, random number selection, and Discord embed updates.
"""

import random
import os

import discord


guessing_games = {}

MAX = int(os.getenv("GUESSING_GAME_MAX_NUMBER"))

# -------------------------
# Embed builder
# -------------------------


def build_embed(state):
    """
    Build a Discord Embed representing current guessing state.

    Args:
        state (dict): The game state containing 'current' and 'target'.

    Returns:
        discord.Embed: Embed ready to send or edit.
    """
    embed = discord.Embed(
        title="🎲 Guess the number",
        description="Guess the number I'm thinking",
        color=0xFF0000 if not state["solved"] else 0x00FF00,
    )

    # Add display progress
    embed.add_field(name="Current guess", value=f"{state['current']}")
    embed.add_field(
        name="Hint",
        value=(
            f"🧠 guess the number between 0 and {MAX}"
            if state["current"] is None
            else (
                "🎉"
                if state["solved"]
                else "⬆️" if state["target"] > state["current"] else "⬇️"
            )
        ),
    )
    embed.add_field(name="Last guess by", value=f"{state["author"]}")
    embed.add_field(name="Guesses", value=f"{state["guesses"]}")

    return embed


# -------------------------
# Game management
# -------------------------


async def start_game(ctx):
    """
    Start a new guessing game in a Discord channel.

    Args:
        ctx: discord.py Context
    """
    if ctx.channel.id in guessing_games:
        await ctx.send("Game already running!", delete_after=5)
        return

    target = random.randint(0, MAX)
    state = {
        "target": target,
        "solved": False,
        "current": None,
        "author": ctx.author.display_name,
        "guesses": 0,
    }

    embed = build_embed(state)
    msg = await ctx.send(embed=embed)
    state["message"] = msg
    guessing_games[ctx.channel.id] = state
    return


def get_state(ctx):
    """
    Retrieve current hangman game state for a channel.

    Args:
        ctx: discord.py Context

    Returns:
        dict | None: Game state or None if no game.
    """
    return guessing_games.get(ctx.channel.id)


async def handle_guess(ctx, state, number):
    """
    Handle a player's number guess.

    Args:
        ctx: discord.py Context
        state (dict): Current game state
        number (int): number guessed
    """
    try:
        guess = int(number)
        if not 0 <= guess <= MAX:
            await ctx.send(
                f"Please guess a number between *0* and *{MAX}*, (otherwise I get headaches :<)",
                delete_after=5,
            )
            return
    except ValueError:
        await ctx.send(
            f"Please guess a number between *0* and *{MAX}*, (otherwise I get headaches :<)",
            delete_after=5,
        )
        return
    process_guess(state, guess)
    state["author"] = ctx.author.display_name

    if state["solved"]:
        await handle_win(ctx, state)
        return
    embed = build_embed(state)
    await state["message"].edit(embed=embed)
    return


def process_guess(state, number):
    """
    Update game state based on a guessed number.

    Args:
        state (dict): Game state
        number (int): Player guess
    """
    state["guesses"] += 1
    state["current"] = number
    if number == state["target"]:
        state["solved"] = True
        return
    return


# -------------------------
# Win/Loss handlers
# -------------------------


async def handle_win(ctx, state):
    """
    Handle a correct guess.

    Args:
        ctx: discord.py Context
        state (dict): Current game state
    """
    embed = build_embed(state)
    await state["message"].edit(embed=embed)
    await ctx.send(
        f"🎉 You guessed it! The number was **{state['target']}**. Solved by {ctx.author.mention}",
        delete_after=5,
    )
    del guessing_games[ctx.channel.id]

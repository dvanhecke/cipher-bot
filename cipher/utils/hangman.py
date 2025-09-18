# Cipher-Bot Hangman logic
# Copyright (c) 2025 dvanhecke
# Licensed under the MIT License

"""
Logic for Hangman minigame.
Contains game state management, word selection, and Discord embed updates.
"""

import random
import discord

# -------------------------
# Game state storage
# -------------------------
HANGMAN_GAMES = {}

HANGMAN_WORDS = [
    "sunny",
    "veny",
    "moony",
    "buni",
    "marsy",
    "uri",
    "pluty",
    "espresso",
    "matcha",
    "croiffle",
    "latte machiato",
    "americano",
]

HANGMAN_PICS = [
    """
   +---+
   |   |
       |
       |
       |
       |
=========""",
    """
   +---+
   |   |
   O   |
       |
       |
       |
=========""",
    """
   +---+
   |   |
   O   |
   |   |
       |
       |
=========""",
    """
   +---+
   |   |
   O   |
  /|   |
       |
       |
=========""",
    """
   +---+
   |   |
   O   |
  /|\\  |
       |
       |
=========""",
    """
   +---+
   |   |
   O   |
  /|\\  |
  /    |
       |
=========""",
    """
   +---+
   |   |
   O   |
  /|\\  |
  / \\  |
       |
=========""",
]

# -------------------------
# Embed builder
# -------------------------


def build_embed(state):
    """
    Build a Discord Embed representing current hangman state.

    Args:
        state (dict): The game state containing 'display' and 'wrong'.

    Returns:
        discord.Embed: Embed ready to send or edit.
    """
    stage = len(state["wrong"])
    embed = discord.Embed(
        title="🔠 Hangman",
        description=f"```{HANGMAN_PICS[stage]}```",
        color=0xFFC300 if stage < len(HANGMAN_PICS) - 1 else 0xFF0000,
    )

    word_display = " ".join(state["display"])
    embed.add_field(name="Word", value=f"```{word_display}```", inline=False)

    wrong_display = ", ".join(state["wrong"]) if state["wrong"] else "None"
    embed.add_field(name="Wrong guesses", value=wrong_display, inline=False)

    return embed


# -------------------------
# Game management
# -------------------------


async def start_game(ctx):
    """
    Start a new hangman game in a Discord channel.

    Args:
        ctx: discord.py Context
    """
    if ctx.channel.id in HANGMAN_GAMES:
        await ctx.send("Game already running!", delete_after=5)
        return

    word = random.choice(HANGMAN_WORDS)
    state = {
        "word": word,
        "display": ["_" for _ in word],
        "wrong": [],
    }

    embed = build_embed(state)
    msg = await ctx.send(embed=embed)
    state["message"] = msg
    HANGMAN_GAMES[ctx.channel.id] = state


def get_state(ctx):
    """
    Retrieve current hangman game state for a channel.

    Args:
        ctx: discord.py Context

    Returns:
        dict | None: Game state or None if no game.
    """
    return HANGMAN_GAMES.get(ctx.channel.id)


async def handle_guess(ctx, state, letter):
    """
    Handle a player's guess in hangman.

    Args:
        ctx: discord.py Context
        state (dict): Current game state
        letter (str): Letter or word guessed
    """
    letter = letter.lower()
    if letter in state["display"] or letter in state["wrong"]:
        await ctx.send("You already guessed that!", delete_after=5)
        return

    process_guess(state, letter)
    embed = build_embed(state)
    await state["message"].edit(embed=embed)

    if is_solved(state):
        await handle_win(ctx, state)
    elif is_hanged(state):
        await handle_loss(ctx, state)


def process_guess(state, letter):
    """
    Update game state based on a guessed letter or word.

    Args:
        state (dict): Game state
        letter (str): Player guess
    """
    if letter == state["word"]:
        for i, ch in enumerate(state["word"]):
            state["display"][i] = ch
        return
    if letter in state["word"]:
        for i, ch in enumerate(state["word"]):
            if ch == letter:
                state["display"][i] = letter
        return
    state["wrong"].append(letter)


def is_solved(state):
    """Return True if the word has been fully guessed."""
    return "_" not in state["display"]


def is_hanged(state):
    """Return True if the player has reached max wrong guesses."""
    return len(state["wrong"]) >= len(HANGMAN_PICS) - 1


# -------------------------
# Win/Loss handlers
# -------------------------


async def handle_win(ctx, state):
    """
    Handle a win in hangman.

    Args:
        ctx: discord.py Context
        state (dict): Current game state
    """
    embed = build_embed(state)
    embed.add_field(name="🏆 Solved by", value=ctx.author.display_name, inline=False)
    await state["message"].edit(embed=embed)
    await ctx.send(
        f"🎉 You guessed it! The word was **{state['word']}**. Solved by {ctx.author.mention}",
        delete_after=5,
    )
    del HANGMAN_GAMES[ctx.channel.id]


async def handle_loss(ctx, state):
    """
    Handle a loss in hangman.

    Args:
        ctx: discord.py Context
        state (dict): Current game state
    """
    for i, ch in enumerate(state["word"]):
        state["display"][i] = ch
    embed = build_embed(state)
    embed.add_field(name="💀 Hanged", value=ctx.author.display_name, inline=False)
    await state["message"].edit(embed=embed)
    await ctx.send(f"💀 You lost! The word was **{state['word']}**.", delete_after=5)
    del HANGMAN_GAMES[ctx.channel.id]

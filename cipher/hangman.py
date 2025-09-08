import random

import discord


hangman_games = {}
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


def build_embed(state):
    stage = len(state["wrong"])
    embed = discord.Embed(
        title="🔠 Hangman",
        description=f"```{HANGMAN_PICS[stage]}```",
        color=0xFFC300 if stage < len(HANGMAN_PICS) - 1 else 0xFF0000,
    )

    # Display word progress
    word_display = " ".join(state["display"])
    embed.add_field(
        name="Word",
        value=f"```{word_display}```",
        inline=False,
    )

    # Show wrong guesses
    wrong_display = ", ".join(state["wrong"]) if state["wrong"] else "None"
    embed.add_field(
        name="Wrong guesses",
        value=wrong_display,
        inline=False,
    )

    return embed


async def start_hangman_game(ctx):
    if ctx.channel.id in hangman_games:
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
    hangman_games[ctx.channel.id] = state
    return


def get_hangman_state(ctx):
    return hangman_games.get(ctx.channel.id)


async def handle_hangman_guess(ctx, state, letter):
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
    return


def is_solved(state):
    return "_" not in state["display"]


def is_hanged(state):
    return len(state["wrong"]) >= len(HANGMAN_PICS) - 1


async def handle_win(ctx, state):
    embed = build_embed(state)
    embed.add_field(name="🏆 Solved by", value=ctx.author.display_name, inline=False)
    await state["message"].edit(embed=embed)
    await ctx.send(
        f"🎉 You guessed it! The word was **{state['word']}**. Solved by {ctx.author.mention}",
        delete_after=5,
    )
    del hangman_games[ctx.channel.id]


async def handle_loss(ctx, state):
    for i, ch in enumerate(state["word"]):
        state["display"][i] = ch
    embed = build_embed(state)
    embed.add_field(name="💀 Hanged", value=ctx.author.display_name, inline=False)
    await state["message"].edit(embed=embed)
    await ctx.send(f"💀 You lost! The word was **{state['word']}**.", delete_after=5)
    del hangman_games[ctx.channel.id]

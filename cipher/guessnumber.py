import random

import discord


guessing_games = {}


def build_embed(state):
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
            "🧠 guess the number between 0 and 100"
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


async def start_guessing_game(ctx):
    if ctx.channel.id in guessing_games:
        await ctx.send("Game already running!", delete_after=5)
        return

    target = random.randint(0, 100)
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


def get_guessing_state(ctx):
    return guessing_games.get(ctx.channel.id)


def process_guess(state, number):
    state["guesses"] += 1
    state["current"] = number
    if number == state["target"]:
        state["solved"] = True
        return
    return


async def handle_win(ctx, state):
    embed = build_embed(state)
    await state["message"].edit(embed=embed)
    await ctx.send(
        f"🎉 You guessed it! The number was **{state['target']}**. Solved by {ctx.author.mention}",
        delete_after=5,
    )
    del guessing_games[ctx.channel.id]


async def handle_guessing_guess(ctx, state, number):
    try:
        guess = int(number)
        if not (0 <= guess <= 100):
            await ctx.send(
                "Please guess a number between *0* and *100*, (otherwise I get headaches :<)",
                delete_after=5,
            )
            return
    except ValueError:
        await ctx.send(
            "Please guess a number between *0* and *100*, (otherwise I get headaches :<)",
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

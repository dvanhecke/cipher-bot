# Cipher-Bot Rock paper scissors logic
# Copyright (c) 2025 dvanhecke
# Licensed under the MIT License

"""
Logic for the rock paper scissors minigame.
Contains parsing of the users input, deciding winner and Discord embed.
"""

import random
import discord

# Choices mapping
WIN_MAP = {"rock": "scissors", "paper": "rock", "scissors": "paper"}

ICON_MAP = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}

CHOICES = ["rock", "paper", "scissors"]


def build_embed(bot_choice: str, user_choice: str, result: str) -> discord.Embed:
    """
    Build a Discord embed representing a Rock-Paper-Scissors game round.

    Args:
        bot_choice (str): Bot's choice
        user_choice (str): User's choice
        result (str): Round result ("user", "bot", "tie")

    Returns:
        discord.Embed: Discord embed ready to send
    """
    embed = discord.Embed(title="🪨📄✂️ Rock-Paper-Scissors", color=discord.Color.blue())
    embed.add_field(name="Your choice", value=ICON_MAP[user_choice], inline=True)
    embed.add_field(name="Bot choice", value=ICON_MAP[bot_choice], inline=True)

    if result == "user":
        embed.add_field(name="Result", value="🎉 You win!", inline=False)
    elif result == "bot":
        embed.add_field(name="Result", value="💀 You lose!", inline=False)
    else:
        embed.add_field(name="Result", value="🤝 Tie!", inline=False)

    return embed


def decide_winner(bot_choice: str, user_choice: str) -> str:
    """
    Decide the winner between bot and user.

    Args:
        bot_choice (str): Bot's choice ("rock", "paper", "scissors")
        user_choice (str): User's choice ("rock", "paper", "scissors")

    Returns:
        str: "user" if user wins, "bot" if bot wins, "tie" if draw
    """
    if bot_choice == user_choice:
        return "tie"
    if WIN_MAP[user_choice] == bot_choice:
        return "user"
    return "bot"


def play_game(user_choice: str) -> dict:
    """
    Play a round of Rock-Paper-Scissors and return the raw result.

    Args:
        user_choice (str): User's choice ("rock", "paper", "scissors")

    Returns:
        dict: {
            "user": str,      # user's choice
            "bot": str,       # bot's choice
            "result": str     # "user", "bot", or "tie"
        }

    Raises:
        ValueError: if user_choice is invalid
    """
    user_choice = user_choice.lower()
    if user_choice not in CHOICES:
        raise ValueError("Please select **rock**, **paper** or **scissors**")
    bot_choice: str = random.choice(CHOICES)
    result = decide_winner(bot_choice, user_choice)
    return {"user": user_choice, "bot": bot_choice, "result": result}

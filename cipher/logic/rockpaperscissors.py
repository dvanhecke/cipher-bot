# Cipher-Bot Rock paper scissors logic
# Copyright (c) 2025 dvanhecke
# Licensed under the MIT License

"""
Logic for the rock paper scissors minigame.
Contains parsing of the users input, deciding winner and Discord embed.
"""

import random
from cipher.utils.minigame import MiniGame


class RockPaperScissorsGame(MiniGame):
    """
    RockPaperScissors Minigame

    This class implements the logic for a single-round Rock Paper Scissors
    game against the bot. It extends the MiniGame base class.

    Features:
    - Accepts a player's choice ("rock", "paper", or "scissors").
    - Randomly selects the bot's choice.
    - Determines the result: win, lose, or tie.
    - Prepares embed-friendly data for Discord display.

    Attributes:
        WIN_MAP (dict): Maps each choice to the choice it defeats.
        ICON_MAP (dict): Maps each choice to a corresponding emoji.
        CHOICES (list): Valid choices for the game.

    Instance Attributes:
        _player_choice (str | None): Player's choice for the current round.
        _bot_choice (str | None): Bot's choice for the current round.
        _result (str | None): Result of the current round as a string.
    """

    WIN_MAP = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
    ICON_MAP = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
    CHOICES = ["rock", "paper", "scissors"]

    def __init__(self, player_choice: str, *args, **kwargs):
        """
        Initialize a new rock paper scissors game.

        Args:
            player_choice (str): the player's choice
        """
        super().__init__(*args, **kwargs)
        self._player_choice = player_choice.lower()
        if player_choice not in self.CHOICES:
            raise ValueError(f"Invalid choice: {player_choice}")

        self._bot_choice = random.choice(self.CHOICES)
        self._result = None

    def play(self, *args, **kwargs) -> None:
        """
        Play one round of RPS against the bot.
        """

        if self.WIN_MAP[self._player_choice] == self._bot_choice:
            self._result = "🎉 You win!"
        elif self.WIN_MAP[self._bot_choice] == self._player_choice:
            self._result = "💀 You lose!"
        else:
            self._result = "🤝 Tie!"

        self._build_embed_data()

    def _build_embed_data(self) -> None:
        """
        Build the embed fields to show the last round.

        Args:
            player_choice (str | None): The player's choice
            bot_choice (str | None): The bot's choice
            result (str | None): The outcome ("win", "lose", "draw")
        """
        fields = {}
        if self._player_choice and self._bot_choice and self._result:
            fields["Player"] = (
                f"{self.ICON_MAP[self._player_choice]} {self._player_choice}",
                True,
            )
            fields["Bot"] = (
                f"{self.ICON_MAP[self._bot_choice]} {self._bot_choice}",
                True,
            )
            fields["Result"] = (self._result, False)
        self._embed_message_data = fields

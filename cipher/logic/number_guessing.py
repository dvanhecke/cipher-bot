# Cipher-Bot number guessing logic
# Copyright (c) 2025 dvanhecke
# Licensed under the MIT License

"""
Logic for numberguessing minigame.
Contains game state management, random number selection, and Discord embed updates.
"""

import random
from cipher.utils.minigame import MiniGame


class NumberGuessing(MiniGame):
    """
    Numbers guessing Minigame

    This class implements the logic for a number guessing
    game against the bot. It extends the MiniGame base class.

    Features:
    - Accepts a player's guess.
    - Randomly selects the bot's choice.
    - Determines the result: win, higher, or lower.
    - Prepares embed-friendly data for Discord display.
    """

    def __init__(self, max_number: int = 10, max_attempts: int | None = None):
        """
        Initialize a new numbers guessing game.

        Args:
            max_number (int): upperbound of the random number defaults to env var
            max_attempts (int | None): maximum attempts to guess the target number defaults to None
        """
        super().__init__(max_attempts=max_attempts)
        self._number = random.randint(0, max_number)
        self._max_number = max_number
        self._result: str = ""

    @property
    def number(self) -> int:
        """Returns the target number"""
        return self._number

    @property
    def result(self) -> int:
        """Returns the result of the guess"""
        return self._result

    def play(self, *args, **kwargs) -> None:
        guess = int(args[0])
        if not 0 <= guess <= self._max_number:
            raise ValueError(
                f"Please select a number between *0* and *{self._max_number}*"
            )

        self._guess_history.append(guess)
        self._attempts += 1

        if guess < self._number:
            self._result = "⬆️"
        elif guess > self._number:
            self._result = "⬇️"
        else:
            self._result = "🎉 Correct!"
            self._active = False

        if self._max_attempts and self._attempts >= self._max_attempts:
            self._active = False

        self._build_embed_data()

    def _build_embed_data(self):
        self._embed_message_data = {
            "Attempts": (str(self._attempts), True),
            "History": (", ".join(map(str, self._guess_history)), True),
            "hint": (self._result, True),
        }

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
    def __init__(self, max_number: int = 100, max_attempts: int | None = None):
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

    def play(self, guess: int) -> str:
        self._guess_history.append(guess)
        self._attempts += 1

        if guess < self._number:
            self._result = "higher"
        elif guess > self._number:
            self._result = "lower"
        else:
            self._result = "correct"
            self._active = False

        if self._max_attempts and self._attempts >= self._max_attempts:
            self._active = False

        self._build_embed_data()

    def _build_embed_data(self):
        self._embed_message_data = {
            "Attempts": (str(self._attempts), True),
            "History": (", ".join(map(str, self._guess_history)), False),
        }

# Cipher-Bot
# Copyright (c) 2025 dvanhecke
# Licensed under the MIT License

"""
Module: cipher.utils.minigame
Handles the base class for all minigames
"""

from abc import ABC, abstractmethod
from typing import List, Any, Mapping


class MiniGame(ABC):
    """
    MiniGame Base Class

    This class provides shared functionality for all minigames:
    - Player tracking
    - Attempt counting
    - Game active/inactive state
    - Guess/move history logging
    - Embed data formatting

    Subclasses should implement game-specific logic (e.g., Number Guessing, RPS).
    """

    def __init__(self, max_attempts: int | None = None) -> None:
        """
        Initialize a new MiniGame.

        Args:
            player (str): The player name or identifier.
            max_attempts (int, optional): Maximum allowed attempts before
                                          the game automatically deactivates.
        """
        self._max_attempts: int | None = max_attempts
        self._attempts: int = 0
        self._active: bool = True
        self._guess_history: List[Any] = []
        self._embed_message_data: Mapping[str, tuple[str, bool]] = None
        self._build_embed_data

    @property
    def attempts(self) -> int:
        """Returns number of attempts"""
        return self._attempts

    @property
    def guess_history(self) -> List[Any]:
        """Returns list of attempts"""
        return self._guess_history

    @property
    def max_attempts(self) -> int:
        """Returns the max_attempts attribute"""
        return self._max_attempts

    @property
    def is_active(self) -> bool:
        """True if the game is still running, False if finished."""
        return self._active

    @is_active.setter
    def is_active(self, value: bool) -> None:
        """Manually activate or deactivate the game."""
        self._active = value

    @property
    def embed_message_data(self) -> dict | None:
        """
        The latest embed representation of the game state.
        """
        return self._embed_message_data

    @abstractmethod
    def _build_embed_data(self):
        """
        Protected method to generate the embed fields for this game.

        Subclasses MUST override this method.

        """
        self._embed_message_data: Mapping[str, tuple[str, bool]] = {}

    @abstractmethod
    def play(self, *args, **kwargs) -> None:
        """
        Abstract method representing the main gameplay loop or action.
        Subclasses MUST override this method.
        """
        pass

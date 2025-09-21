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
        self._embed_message_data: Mapping[str, tuple[str, bool]] = (
            self._build_embed_data()
        )

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
    def _build_embed_data(self) -> Mapping[str, tuple[str, bool]]:
        """
        Protected method to generate the embed fields for this game.

        Subclasses MUST override this method.

        Returns:
            Mapping[str, Tuple[str, bool]]: Field name -> (value, inline flag)
        """
        return {}

    @abstractmethod
    def play(self, *args, **kwargs) -> Any:
        """
        Abstract method representing the main gameplay loop or action.
        Subclasses MUST override this method.
        """
        pass

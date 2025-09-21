# tests/test_rps.py
import pytest
from cipher.logic.rockpaperscissors import RockPaperScissorsGame

VALID_CHOICES = ["rock", "paper", "scissors"]


def test_valid_choices():
    """Test that all valid choices return a result without errors."""
    for choice in VALID_CHOICES:
        game = RockPaperScissorsGame(choice)
        game.play()
        assert game._player_choice == choice
        assert game._bot_choice in VALID_CHOICES
        assert game._result in ["🎉 You win!", "💀 You lose!", "🤝 Tie!"]
        embed_data = game.embed_message_data
        assert "Player" in embed_data
        assert "Bot" in embed_data
        assert "Result" in embed_data


def test_invalid_choice():
    """Test that an invalid choice raises a ValueError."""
    with pytest.raises(ValueError):
        RockPaperScissorsGame("lizard")


def test_embed_data_structure():
    """Test that embed data fields have correct types."""
    game = RockPaperScissorsGame("rock")
    game.play()
    embed_data = game.embed_message_data
    for key, value in embed_data.items():
        assert isinstance(key, str)
        assert isinstance(value, tuple)
        assert isinstance(value[0], str)
        assert isinstance(value[1], bool)

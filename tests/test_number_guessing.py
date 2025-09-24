# tests/test_number_guessing.py
import pytest
from cipher.logic.number_guessing import NumberGuessing


def test_guess_correct(monkeypatch):
    """Test guessing the correct number."""
    game = NumberGuessing()
    # Force the number to 5
    monkeypatch.setattr(game, "_number", 5)

    game.play(game.number)
    assert game.result == "correct"
    assert game.is_active is False
    assert game.attempts == 1
    assert game.guess_history == [5]


def test_guess_too_low(monkeypatch):
    """Test guessing lower than the target number."""
    game = NumberGuessing()
    monkeypatch.setattr(game, "_number", 7)

    game.play(5)
    assert game.result == "higher"
    assert game.is_active is True
    assert game.attempts == 1
    assert game.guess_history == [5]


def test_guess_too_high(monkeypatch):
    """Test guessing higher than the target number."""
    game = NumberGuessing()
    monkeypatch.setattr(game, "_number", 3)

    game.play(5)
    assert game.result == "lower"
    assert game.is_active is True
    assert game.attempts == 1
    assert game.guess_history == [5]


def test_max_attempts(monkeypatch):
    """Test that max_attempts disables the game."""
    game = NumberGuessing(max_attempts=2)
    monkeypatch.setattr(game, "_number", 8)

    assert game.is_active
    game.play(1)  # attempt 1
    assert game.is_active
    game.play(2)  # attempt 2, hits max_attempts
    assert game.is_active is False


def test_embed_data(monkeypatch):
    """Test that _build_embed_data returns correct structure."""
    game = NumberGuessing()
    monkeypatch.setattr(game, "_number", 5)

    game.play(3)
    embed_data = game.embed_message_data
    assert isinstance(embed_data, dict)
    assert "Attempts" in embed_data
    assert "History" in embed_data
    assert embed_data["Attempts"][0] == "1"
    assert embed_data["Attempts"][1] is True
    assert embed_data["History"][0] == "3"
    assert embed_data["History"][1] is False


def test_arg_parsing():
    """Test that the argument gets parsed correctly"""
    game = NumberGuessing()
    with pytest.raises(ValueError):
        game.play("test")
    with pytest.raises(ValueError):
        game.play(1000)
    assert game.guess_history == []
    assert game.attempts == 0

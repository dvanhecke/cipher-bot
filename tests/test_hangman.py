# tests/test_hangman.py
# Copyright (c) 2025 dvanhecke
# Licensed under the MIT License

"""
Tests for the Hangman minigame logic.
"""

import pytest
from cipher.logic.hangman import Hangman


def test_game_starts_active():
    game = Hangman(word="python", max_attempts=6)
    assert game.is_active
    assert game.word == "python"
    assert game.remaining_attempts == 6


def test_correct_guess_reveals_letters():
    game = Hangman(word="test", max_attempts=6)
    game.play("t")
    assert game.display_word == "t _ _ t"
    assert game.remaining_attempts == 6
    assert game.is_active


def test_incorrect_guess_reduces_attempts():
    game = Hangman(word="test", max_attempts=6)
    game.play("x")
    assert game.remaining_attempts == 5
    assert "x" in game.wrong_guesses


def test_win_condition():
    game = Hangman(word="hi", max_attempts=6)
    game.play("h")
    game.play("i")
    assert not game.is_active
    assert game.result == "🎉 You win!"


def test_lose_condition():
    game = Hangman(word="hi", max_attempts=2)
    game.play("x")
    game.play("y")
    assert not game.is_active
    assert game.result == "💀 You lose!"


def test_invalid_input_raises():
    game = Hangman(word="hi", max_attempts=6)
    with pytest.raises(ValueError):
        game.play("123")  # invalid guess


def test_embed_data_structure():
    game = Hangman(word="hi", max_attempts=6)
    game.play("h")
    fields = game.embed_message_data
    assert isinstance(fields, dict)
    assert "Word" in fields
    assert "Attempts left" in fields

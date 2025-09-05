import pytest
import time
from src.hangman import select_word, select_phrase, HangmanGame

def test_select_word():
    word = select_word()
    assert isinstance(word, str)
    assert len(word) > 0
    assert word.isalpha()

def test_select_phrase():
    phrase = select_phrase()
    assert isinstance(phrase, str)
    assert len(phrase) > 0
    assert all(c.isalpha() or c.isspace() for c in phrase)

def test_initialize_game_word():
    game = HangmanGame("test")
    assert game.display_word == "_ _ _ _"  # Changed from "____"
    assert game.guessed_letters == set()
    assert game.lives == 6

def test_initialize_game_phrase():
    game = HangmanGame("test phrase")
    assert game.display_word == "_ _ _ _   _ _ _ _ _ _"  # Changed from "____ ______"
    assert game.guessed_letters == set()
    assert game.lives == 6

def test_correct_guess():
    game = HangmanGame("test")
    result = game.guess_letter('t')
    assert result is True
    assert "t" in game.display_word
    assert game.lives == 6

def test_incorrect_guess():
    game = HangmanGame("test")
    result = game.guess_letter('x')
    assert result is False
    assert game.display_word == "_ _ _ _"  # Changed from "____"
    assert game.lives == 5

def test_already_guessed_letter():
    game = HangmanGame("test")
    game.guess_letter('t')
    result = game.guess_letter('t')
    assert result is None
    assert game.lives == 6

def test_game_won():
    game = HangmanGame("test")
    game.guess_letter('t')
    game.guess_letter('e')
    game.guess_letter('s')
    assert game.is_won() is True
    assert game.is_game_over() is True

def test_game_lost():
    game = HangmanGame("test", lives=2)
    game.guess_letter('x')
    game.guess_letter('y')
    assert game.is_lost() is True
    assert game.is_game_over() is True

# Fixed timer tests - using monkeypatch instead of mocker
def test_timer_expiration():
    game = HangmanGame("test")
    game.start_time = time.time() - 20  # Force 20 seconds elapsed
    game.time_limit = 15
    
    assert game.is_time_up() is True
    assert game.lives == 5  # Life deducted

def test_timer_not_expired():
    game = HangmanGame("test")
    game.start_time = time.time() - 10  # Only 10 seconds elapsed
    game.time_limit = 15
    
    assert game.is_time_up() is False
    assert game.lives == 6  # No life deducted

def test_complete_game_flow():
    game = HangmanGame("test", lives=6)
    assert game.guess_letter('t') is True
    assert game.guess_letter('x') is False
    game.guess_letter('e')
    game.guess_letter('s')
    assert game.is_won() is True
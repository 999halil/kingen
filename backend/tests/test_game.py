import pytest
from kingen.engine.card import Card, Suit
from kingen.engine.player import Player
from kingen.engine.contract import ContractType
from kingen.engine.game import Game


def test_game_initialization():
    players = [Player(id=f"p{i}", name=f"Speler {i}") for i in range(1, 5)]
    game = Game(players=players)

    assert len(game.contract_queue) == 10
    assert game.current_round_index == 0
    assert all(score == 0 for score in game.total_scores.values())


def test_start_next_round():
    players = [Player(id=f"p{i}", name=f"Speler {i}") for i in range(1, 5)]
    game = Game(players=players)

    current_round = game.start_next_round()
    assert current_round.contract == ContractType.MIN_SLAGEN
    assert game.current_round is not None

    # Controleer of elke speler nu 13 kaarten heeft ontvangen
    for player in game.players:
        assert len(player.hand) == 13


def test_troef_ronde_vereist_troefkleur():
    players = [Player(id=f"p{i}", name=f"Speler {i}") for i in range(1, 5)]
    game = Game(players=players)
    game.current_round_index = 6  # Index 6 is de eerste troefronde

    with pytest.raises(ValueError, match="Bij een troefronde moet er een troefkleur worden gekozen."):
        game.start_next_round()

    # Met troefkleur moet het wel werken
    round_troef = game.start_next_round(trump_suit=Suit.SPADES)
    assert round_troef.trump_suit == Suit.SPADES
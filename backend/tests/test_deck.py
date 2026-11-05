import pytest
from kingen.engine.card import Card, Rank, Suit
from kingen.engine.deck import Deck


def test_deck_initialization():
    deck = Deck()
    assert len(deck.cards) == 52


def test_deck_deal():
    deck = Deck()
    hands = deck.deal()
    
    assert len(hands) == 4
    for hand in hands:
        assert len(hand) == 13


def test_card_representation():
    card = Card(suit=Suit.HEARTS, rank=Rank.KING)
    assert str(card) == "K♥"
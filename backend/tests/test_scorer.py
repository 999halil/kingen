import pytest
from kingen.engine.card import Card, Rank, Suit
from kingen.engine.trick import Trick
from kingen.engine.contract import ContractType
from kingen.engine.scorer import ScoreCalculator

def create_mock_trick(cards: list[Card]) -> Trick:
    trick = Trick()
    for i, card in enumerate(cards):
        trick.add_card(f"p{i+1}", card)
    return trick

def test_min_dames_score():
    trick = create_mock_trick([
        Card(suit=Suit.HEARTS, rank=Rank.QUEEN),
        Card(suit=Suit.SPADES, rank=Rank.QUEEN),
        Card(suit=Suit.CLUBS, rank=Rank.TEN),
        Card(suit=Suit.DIAMONDS, rank=Rank.TWO)
    ])
    score = ScoreCalculator.calculate_trick_score(trick, ContractType.MIN_DAMES, 0)
    assert score == -4  # 2 dames = -4 punten

def test_harten_heer_score():
    trick = create_mock_trick([
        Card(suit=Suit.HEARTS, rank=Rank.KING),
        Card(suit=Suit.SPADES, rank=Rank.TEN),
        Card(suit=Suit.CLUBS, rank=Rank.TEN),
        Card(suit=Suit.DIAMONDS, rank=Rank.TWO)
    ])
    score = ScoreCalculator.calculate_trick_score(trick, ContractType.HARTEN_HEER, 0)
    assert score == -5

def test_zevende_en_laatste_score():
    trick = create_mock_trick([
        Card(suit=Suit.HEARTS, rank=Rank.TWO),
        Card(suit=Suit.SPADES, rank=Rank.TWO),
        Card(suit=Suit.CLUBS, rank=Rank.TWO),
        Card(suit=Suit.DIAMONDS, rank=Rank.TWO)
    ])
    # 7e slag (index 6)
    assert ScoreCalculator.calculate_trick_score(trick, ContractType.Zevende_en_Laatste, 6) == -3
    # 13e slag (index 12)
    assert ScoreCalculator.calculate_trick_score(trick, ContractType.Zevende_en_Laatste, 12) == -2
    # Willekeurige andere slag (index 3)
    assert ScoreCalculator.calculate_trick_score(trick, ContractType.Zevende_en_Laatste, 3) == 0
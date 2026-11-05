import pytest
from kingen.engine.card import Card, Rank, Suit
from kingen.engine.player import Player
from kingen.engine.contract import ContractType
from kingen.engine.round import Round

def test_bekennen_regel():
    # Speler 1 heeft Harten 10, Speler 2 heeft Harten 2 en Schoppen Aas
    p1 = Player(id="p1", name="Alice", hand=[Card(suit=Suit.HEARTS, rank=Rank.TEN)])
    p2 = Player(id="p2", name="Bob", hand=[
        Card(suit=Suit.HEARTS, rank=Rank.TWO),
        Card(suit=Suit.SPADES, rank=Rank.ACE)
    ])
    p3 = Player(id="p3", name="Charlie", hand=[Card(suit=Suit.CLUBS, rank=Rank.TWO)])
    p4 = Player(id="p4", name="Dave", hand=[Card(suit=Suit.DIAMONDS, rank=Rank.TWO)])

    round_game = Round(contract=ContractType.MIN_SLAGEN, players=[p1, p2, p3, p4])

    # P1 komt uit met Harten 10
    round_game.play_turn("p1", p1.hand[0])

    # P2 is nu aan de beurt. Controleer of zijn enige geldige kaart de Harten 2 is
    valid_cards_p2 = round_game.get_valid_cards(p2)
    assert len(valid_cards_p2) == 1
    assert valid_cards_p2[0] == Card(suit=Suit.HEARTS, rank=Rank.TWO)

    # Probeer een illegale kaart op te gooien (Schoppen Aas)
    with pytest.raises(ValueError, match="Mag .* niet spelen. Bekennen is verplicht!"):
        round_game.play_turn("p2", Card(suit=Suit.SPADES, rank=Rank.ACE))

def test_volledige_slag_resolutie():
    p1 = Player(id="p1", name="Alice", hand=[Card(suit=Suit.HEARTS, rank=Rank.TEN)])
    p2 = Player(id="p2", name="Bob", hand=[Card(suit=Suit.HEARTS, rank=Rank.JACK)])
    p3 = Player(id="p3", name="Charlie", hand=[Card(suit=Suit.HEARTS, rank=Rank.QUEEN)])
    p4 = Player(id="p4", name="Dave", hand=[Card(suit=Suit.HEARTS, rank=Rank.KING)])

    round_game = Round(contract=ContractType.MIN_SLAGEN, players=[p1, p2, p3, p4])

    # Iedereen speelt netjes zijn Harten kaart
    round_game.play_turn("p1", p1.hand[0])
    round_game.play_turn("p2", p2.hand[0])
    round_game.play_turn("p3", p3.hand[0])
    round_game.play_turn("p4", p4.hand[0])

    # De slag is vol. P4 (Dave) had de hoogste kaart (Harten Heer)
    assert round_game.trick_index == 1
    assert len(round_game.past_tricks) == 1
    
    # Contract was MIN_SLAGEN, dus Dave moet -1 punt hebben
    assert round_game.scores["p4"] == -1
    assert round_game.scores["p1"] == 0

    # Omdat P4 won, is het nu de beurt aan index 3 (Dave)
    assert round_game.current_player_index == 3
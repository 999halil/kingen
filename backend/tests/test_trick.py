import pytest
from kingen.engine.card import Card, Rank, Suit
from kingen.engine.trick import Trick
from kingen.engine.player import Player

def test_player_play_card():
    player = Player(id="p1", name="Alice", hand=[Card(suit=Suit.HEARTS, rank=Rank.TEN)])
    played = player.play_card(Card(suit=Suit.HEARTS, rank=Rank.TEN))
    
    assert played == Card(suit=Suit.HEARTS, rank=Rank.TEN)
    assert len(player.hand) == 0

def test_trick_winner_no_trump():
    trick = Trick()
    trick.add_card("p1", Card(suit=Suit.HEARTS, rank=Rank.TEN))  # Lead suit is Hearts
    trick.add_card("p2", Card(suit=Suit.HEARTS, rank=Rank.KING)) # P2 overneemt
    trick.add_card("p3", Card(suit=Suit.SPADES, rank=Rank.ACE))  # P3 kan niet bekennen, gooit Schoppen Aas weg
    trick.add_card("p4", Card(suit=Suit.HEARTS, rank=Rank.TWO))  # P4 bekent met een twee
    
    assert trick.lead_suit == Suit.HEARTS
    assert trick.get_winner() == "p2"  # Harten Heer wint, Schoppen Aas telt niet mee

def test_trick_winner_with_trump():
    trick = Trick(trump_suit=Suit.SPADES)
    trick.add_card("p1", Card(suit=Suit.HEARTS, rank=Rank.ACE))  # Lead suit is Hearts
    trick.add_card("p2", Card(suit=Suit.HEARTS, rank=Rank.KING))
    trick.add_card("p3", Card(suit=Suit.SPADES, rank=Rank.TWO))  # P3 snijdt in met Schoppen Twee (Troef)
    trick.add_card("p4", Card(suit=Suit.HEARTS, rank=Rank.QUEEN))
    
    assert trick.get_winner() == "p3"  # Schoppen Twee wint door troef
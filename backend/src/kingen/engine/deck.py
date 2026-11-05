import random
from typing import List
from kingen.engine.card import Card, Suit, Rank

class Deck:
    def __init__(self) -> None:
        self.cards: List[Card] = [
            Card(suit=suit, rank=rank) 
            for suit in Suit 
            for rank in Rank
        ]

    def shuffle(self) -> None:
        random.shuffle(self.cards)
    def deal(self) -> List[List[Card]]:
        """Deelt de 52 kaarten gelijkmatig over 4 spelers (13 kaarten elk)."""
        if len(self.cards) != 52:
            raise ValueError("Het deck moet 52 kaarten bevatten om te delen.")
        
        return [self.cards[i * 13:(i + 1) * 13] for i in range(4)]      
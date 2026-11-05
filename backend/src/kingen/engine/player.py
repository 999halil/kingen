from typing import List
from pydantic import BaseModel, Field
from kingen.engine.card import Card

class Player(BaseModel):
    id: str
    name: str
    hand: List[Card] = Field(default_factory=list)

    def play_card(self, card: Card) -> Card:
        """Speelt een kaart uit de hand van de speler en verwijdert deze."""
        if card not in self.hand:
            raise ValueError(f"{self.name} heeft de kaart {card} niet in de hand.")
        
        self.hand.remove(card)
        return card
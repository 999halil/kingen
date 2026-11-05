from typing import Dict, Optional
from pydantic import BaseModel, Field
from kingen.engine.card import Card, Suit

class Trick(BaseModel):
    # Dictionary die bijhoudt welke speler (ID) welke kaart speelde
    played_cards: Dict[str, Card] = Field(default_factory=dict)
    trump_suit: Optional[Suit] = None

    @property
    def lead_suit(self) -> Optional[Suit]:
        """Bepaalt de kleur die gevraagd is (de kleur van de eerst gespeelde kaart)."""
        if not self.played_cards:
            return None
        # De eerste kaart in de dictionary bepaalt de gevraagde kleur
        first_card = list(self.played_cards.values())[0]
        return first_card.suit

    def add_card(self, player_id: str, card: Card) -> None:
        """Voegt een kaart toe aan de slag."""
        if len(self.played_cards) >= 4:
            raise ValueError("De slag is al vol (4 kaarten).")
        if player_id in self.played_cards:
            raise ValueError(f"Speler {player_id} heeft al een kaart gespeeld in deze slag.")
        
        self.played_cards[player_id] = card

    def get_winner(self) -> str:
        """Bepaalt welke speler (ID) de slag wint op basis van Kingen-regels."""
        if len(self.played_cards) < 4:
            raise ValueError("De slag is nog niet compleet.")

        lead_suit = self.lead_suit
        winning_player = None
        best_card = None

        for player_id, card in self.played_cards.items():
            if best_card is None:
                best_card = card
                winning_player = player_id
                continue

            # Logica 1: De kaart is een troefkaart
            if self.trump_suit and card.suit == self.trump_suit:
                if best_card.suit != self.trump_suit or card.rank > best_card.rank:
                    best_card = card
                    winning_player = player_id
            
            # Logica 2: De kaart volgt de gevraagde kleur (en de huidige winnaar heeft geen troef)
            elif card.suit == lead_suit and (not self.trump_suit or best_card.suit != self.trump_suit):
                if card.rank > best_card.rank:
                    best_card = card
                    winning_player = player_id

        return winning_player
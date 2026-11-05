from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from kingen.engine.card import Card, Suit
from kingen.engine.player import Player
from kingen.engine.trick import Trick
from kingen.engine.contract import ContractType
from kingen.engine.scorer import ScoreCalculator

class Round(BaseModel):
    contract: ContractType
    players: List[Player]
    scores: Dict[str, int] = Field(default_factory=dict)
    current_trick: Trick = Field(default_factory=Trick)
    past_tricks: List[Trick] = Field(default_factory=list)
    trick_index: int = 0  # Index van de huidige slag (0 tot 12)
    current_player_index: int = 0  # Index van de speler die aan de beurt is
    trump_suit: Optional[Suit] = None  # Alleen relevant voor TROEF contract

    def model_post_init(self, __context) -> None:
        """Initialiseert scores en troef-instellingen na het aanmaken van de klasse."""
        if not self.scores:
            self.scores = {p.id: 0 for p in self.players}
        if self.contract == ContractType.TROEF and not self.trump_suit:
            raise ValueError("Bij een troef-contract moet een troefkleur gekozen zijn.")
        if self.trump_suit:
            self.current_trick.trump_suit = self.trump_suit

    def get_valid_cards(self, player: Player) -> List[Card]:
        """Bepaalt welke kaarten de speler mag opgooien (verplicht bekennen)."""
        lead_suit = self.current_trick.lead_suit
        if not lead_suit:
            return player.hand  # Mag alles uitkomen
        
        cards_of_lead_suit = [c for c in player.hand if c.suit == lead_suit]
        if cards_of_lead_suit:
            return cards_of_lead_suit  # Je hebt de kleur, dus je MOET bekennen
        
        return player.hand  # Je hebt de kleur niet, je mag elke kaart opgooien

    def play_turn(self, player_id: str, card: Card) -> None:
        """Verwerkt de zet van een speler en controleert de regels."""
        if self.trick_index >= 13:
            raise ValueError("De ronde is al afgelopen (13 slagen gespeeld).")

        current_player = self.players[self.current_player_index]
        if current_player.id != player_id:
            raise ValueError(f"Het is niet de beurt aan speler {player_id}.")
        
        valid_cards = self.get_valid_cards(current_player)
        if card not in valid_cards:
            raise ValueError(f"Mag {card} niet spelen. Bekennen is verplicht!")
        
        # Kaart spelen en aan slag toevoegen
        current_player.play_card(card)
        self.current_trick.add_card(current_player.id, card)

        # Check of de slag vol is (4 kaarten)
        if len(self.current_trick.played_cards) == 4:
            self._resolve_trick()
        else:
            self.current_player_index = (self.current_player_index + 1) % 4

    def _resolve_trick(self) -> None:
        """Rondt de slag af, berekent scores en bereidt de volgende slag voor."""
        winner_id = self.current_trick.get_winner()
        
        # Punten berekenen en toewijzen
        score = ScoreCalculator.calculate_trick_score(
            self.current_trick, self.contract, self.trick_index
        )
        self.scores[winner_id] += score
        
        # Slag opslaan
        self.past_tricks.append(self.current_trick)
        self.trick_index += 1
        
        # Nieuwe slag voorbereiden, tenzij het spel klaar is
        if self.trick_index < 13:
            self.current_trick = Trick(trump_suit=self.trump_suit)
            self.current_player_index = next(
                i for i, p in enumerate(self.players) if p.id == winner_id
            )



from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from kingen.engine.card import Card, Suit
from kingen.engine.deck import Deck
from kingen.engine.player import Player
from kingen.engine.contract import ContractType
from kingen.engine.round import Round


class Game(BaseModel):
    players: List[Player]
    total_scores: Dict[str, int] = Field(default_factory=dict)
    round_history: List[Round] = Field(default_factory=list)
    current_round: Optional[Round] = None
    current_round_index: int = 0

    # De vaste volgorde van de 10 rondes in een potje Kingen
    contract_queue: List[ContractType] = Field(
        default_factory=lambda: [
            ContractType.MIN_SLAGEN,
            ContractType.MIN_HARTEN,
            ContractType.MIN_HEREN_BOEREN,
            ContractType.MIN_DAMES,
            ContractType.HARTEN_HEER,
            ContractType.Zevende_en_Laatste,
            ContractType.TROEF,
            ContractType.TROEF,
            ContractType.TROEF,
            ContractType.TROEF,
        ]
    )

    def model_post_init(self, __context) -> None:
        """Initialiseert de cumulatieve scorebord-stand voor alle 4 spelers."""
        if not self.total_scores:
            self.total_scores = {p.id: 0 for p in self.players}

    @property
    def is_finished(self) -> bool:
        """Geeft True terug als alle 10 contracten zijn afgerond."""
        return self.current_round_index >= len(self.contract_queue)

    def start_next_round(self, trump_suit: Optional[Suit] = None) -> Round:
        """Start een nieuwe ronde, schudt en deelt de kaarten."""
        if self.is_finished:
            raise ValueError("Het spel is al afgelopen. Alle contracten zijn gespeeld.")

        contract = self.contract_queue[self.current_round_index]

        if contract == ContractType.TROEF and not trump_suit:
            raise ValueError("Bij een troefronde moet er een troefkleur worden gekozen.")

        # Vers deck schudden en delen aan de 4 spelers
        deck = Deck()
        deck.shuffle()
        hands = deck.deal()

        for player, hand in zip(self.players, hands):
            player.hand = hand

        # De eerste speler die uitkomt schuift per ronde 1 plek door
        starter_index = self.current_round_index % 4

        self.current_round = Round(
            contract=contract,
            players=self.players,
            trump_suit=trump_suit,
            current_player_index=starter_index,
        )
        return self.current_round

    def play_turn(self, player_id: str, card: Card) -> None:
        """Verwerkt een zet in de actieve ronde en telt de punten op bij het einde van de ronde."""
        if not self.current_round:
            raise ValueError("Er is geen actieve ronde. Start eerst een nieuwe ronde met start_next_round().")

        self.current_round.play_turn(player_id, card)

        # Als alle 13 slagen van de ronde gespeeld zijn, verwerken we de scores
        if self.current_round.trick_index == 13:
            self._finish_round()

    def _finish_round(self) -> None:
        """Sluit de actieve ronde af en telt de ronde-score op bij de totaalstand."""
        if not self.current_round:
            return

        for p_id, score in self.current_round.scores.items():
            self.total_scores[p_id] += score

        self.round_history.append(self.current_round)
        self.current_round = None
        self.current_round_index += 1
from typing import List
from kingen.engine.card import Card, Suit, Rank
from kingen.engine.contract import ContractType
from kingen.engine.trick import Trick

class ScoreCalculator:
    
    @staticmethod
    def calculate_trick_score(trick: Trick, contract: ContractType, trick_index: int) -> int:
        """
        Berekent de score van één specifieke slag op basis van het actieve contract.
        trick_index is de index van de slag (0 tot 12).
        """
        score = 0
        cards_in_trick = list(trick.played_cards.values())

        if contract == ContractType.MIN_SLAGEN:
            score -= 1  # -1 per gehaalde slag

        elif contract == ContractType.MIN_HARTEN:
            for card in cards_in_trick:
                if card.suit == Suit.HEARTS:
                    score -= 1  # -1 per hartenkaart

        elif contract == ContractType.MIN_HEREN_BOEREN:
            for card in cards_in_trick:
                if card.rank in (Rank.KING, Rank.JACK):
                    score -= 1  # -1 per heer of boer

        elif contract == ContractType.MIN_DAMES:
            for card in cards_in_trick:
                if card.rank == Rank.QUEEN:
                    score -= 2  # -2 per dame (vrouw)

        elif contract == ContractType.HARTEN_HEER:
            for card in cards_in_trick:
                if card.suit == Suit.HEARTS and card.rank == Rank.KING:
                    score -= 5  # -5 voor de Harten Heer

        elif contract == ContractType.Zevende_en_Laatste:
            if trick_index == 6:  # 7e slag (0-indexed)
                score -= 3
            elif trick_index == 12: # 13e en laatste slag
                score -= 2

        elif contract == ContractType.TROEF:
            score += 1  # +1 per gehaalde slag in een troefronde

        return score
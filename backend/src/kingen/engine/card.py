from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

class Suit(str, Enum):
    HEARTS = "H"
    DIAMONDS = "D"
    CLUBS = "C"
    SPADES = "S"

class Rank(int, Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Card(BaseModel):
    suit: Suit
    rank: Rank

    model_config = ConfigDict(frozen=True)

    def __str__(self) -> str:

        symbols = {
            Suit.HEARTS: "♥",
            Suit.DIAMONDS: "♦",
            Suit.CLUBS: "♣",
            Suit.SPADES: "♠"
        }
        rank_names = {
            11:"J", 12:"Q", 13:"K", 14:"A"
        }
        rank_str = rank_names.get(self.rank.value, str(self.rank.value))
        return f"{rank_str}{symbols[self.suit]}"
    
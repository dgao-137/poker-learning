
import random
from enum import Enum
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

class Rank(Enum):
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

@dataclass
class Card:
    rank: Rank
    suit: Suit
    
    def __str__(self):
        rank_str = {
            Rank.ACE: "A", Rank.KING: "K", Rank.QUEEN: "Q", Rank.JACK: "J", Rank.TEN: "T"
        }.get(self.rank, str(self.rank.value))
        return f"{rank_str}{self.suit.value}"
    
class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in Rank for suit in Suit]
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self) -> Card:
        return self.cards.pop()
    
class HandRank(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

# evaluates the current hand to determine its rank
# returns a tuple of (hand_rank, high_card_value)
# both rank and high card value are used to compare hands
def evaluate_hand(hole_cards: List[Card], community_cards: List[Card]) -> Tuple[HandRank, int]:
    all_cards = hole_cards + community_cards
    ranks = [card.rank.value for card in all_cards]
    suits = [card.suit for card in all_cards]
    
    # first find the counts for each rank to determine pairs, three of a kind, etc.
    rank_counts = {}
    for rank in ranks:
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
    
    # check for flush (cards of the same suit)
    suit_counts = {}
    for suit in suits:
        suit_counts[suit] = suit_counts.get(suit, 0) + 1
    is_flush = any(count >= 5 for count in suit_counts.values())
    
    # check for straight (cards in consecutive order)
    sorted_ranks = sorted(set(ranks))
    is_straight = False
    if len(sorted_ranks) >= 5:
        for i in range(len(sorted_ranks) - 4):
            if sorted_ranks[i+4] - sorted_ranks[i] == 4:
                is_straight = True
                break
    
    # Determine hand rank
    counts = sorted(rank_counts.values(), reverse=True)
    high_card = max(ranks)
    
    if is_flush and sorted_ranks == [10, 11, 12, 13, 14]:  # Check for Royal Flush
        return HandRank.ROYAL_FLUSH, high_card
    if is_straight and is_flush:
        return HandRank.STRAIGHT_FLUSH, high_card
    elif 4 in counts:
        return HandRank.FOUR_KIND, high_card
    elif 3 in counts and 2 in counts:
        return HandRank.FULL_HOUSE, high_card
    elif is_flush:
        return HandRank.FLUSH, high_card
    elif is_straight:
        return HandRank.STRAIGHT, high_card
    elif 3 in counts:
        return HandRank.THREE_KIND, high_card
    elif counts.count(2) >= 2:
        return HandRank.TWO_PAIR, high_card
    elif 2 in counts:
        return HandRank.PAIR, high_card
    else:
        return HandRank.HIGH_CARD, high_card

# player actions in the game
class Action(Enum):
    FOLD = "fold"
    CALL = "call" 
    RAISE = "raise"

"""Solution to day 7 of Advent of Code"""

from get_input import get_input, line_parser
from collections import Counter


class Hand:
    TYPES = (
        (1, 1, 1, 1, 1),  # High card
        (2, 1, 1, 1),     # Pair
        (2, 2, 1),        # Two Pair
        (3, 1, 1),        # Three of a kind
        (3, 2),           # Full house
        (4, 1),           # Four of a kind
        (5,),             # Five of a kind
    )

    def __init__(self, values, bid, order):
        self.order = order
        self.bid = bid
        self.cards = list(self.order.index(v) for v in values)

    def __lt__(self, other):
        return (self.rank, self.cards) < (other.rank, other.cards)

    def __repr__(self):
        return ''.join(self.order[c] for c in self.cards)

    __str__ = __repr__

    @property
    def rank(self):
        counts = sorted(Counter(self.cards).values(), reverse=True)
        return self.TYPES.index(tuple(counts))

    def best_hand(self):
        counts = sorted(Counter(c for c in self.cards if c != self.order.index('J')).values(), reverse=True)
        if counts == []:
            counts = [5]
        # Just assign jokers to the hightest value
        # 5 or 4 jokers always make five of a kind
        # 3 jokers can be (1, 1) or (2,)
        # 2 jokers can be (1, 1, 1), (2, 1), or (3,)
        # 1 jokers can be (1, 1, 1, 1), (2, 1, 1), (3, 1) or (4,)
        counts[0] += len(self.cards) - sum(counts)
        return (self.TYPES.index(tuple(counts)), self.cards)


def part1(hands):
    order = list("23456789TJQKA")
    hands = sorted(Hand(*hand, order=order) for hand in hands)
    return sum(h.bid * p for p, h in enumerate(hands, 1))


def part2(hands):
    order = list("J23456789TQKA")
    hands = sorted((Hand(*hand, order=order) for hand in hands), key=lambda h: h.best_hand())
    return sum(h.bid * p for p, h in enumerate(hands, 1))


TEXT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


def test_part1():
    hands = line_parser(TEXT, parse=parse)
    assert part1(hands) == 6440


def test_part2():
    hands = line_parser(TEXT, parse=parse)
    assert part2(hands) == 5905


def parse(line):
    cards, bet = line.split(' ')
    return (cards, int(bet))


if __name__ == "__main__":
    LINES = line_parser(get_input(day=7, year=2023), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

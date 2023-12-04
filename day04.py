"""Solution to day 4 of Advent of Code"""

from get_input import get_input, line_parser
import re


def part1(games):
    total = 0
    for _, win, mine in games:
        common = set(win) & set(mine)
        total += int(2 ** (len(common) - 1))
    return total


def part2(games):
    counts = {g[0]: 0 for g in games}
    for c, win, mine in games:
        common = set(win) & set(mine)
        counts[c] += 1
        for n in range(c+1, c+1+len(common)):
            counts[n] += counts[c]
    return sum(counts.values())


TEXT = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def test_part1():
    games = line_parser(TEXT, parse=parse)
    assert part1(games) == 13


def test_part2():
    games = line_parser(TEXT, parse=parse)
    assert part2(games) == 30


def parse(line):
    m = re.match(r"Card +(\d+):((?: +\d+)+) \|((?: +\d+)+)", line)
    num = int(m.group(1))
    winning = tuple(int(n) for n in re.findall(r"\d+", m.group(2)))
    mine = tuple(int(n) for n in re.findall(r"\d+", m.group(3)))
    return (num, winning, mine)


if __name__ == "__main__":
    LINES = line_parser(get_input(day=4, year=2023), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

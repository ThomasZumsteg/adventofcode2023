"""Solution to day 2 of Advent of Code"""

from get_input import get_input, line_parser
from operator import mul
from functools import reduce
import re


def part1(games):
    total = 0
    maxium = {'red': 12, 'green': 13, 'blue': 14}
    for gid, subsets in games:
        if all(subset.get(name, 0) <= val for name, val in maxium.items() for subset in subsets):
            total += gid
    return total


def part2(games):
    total = 0
    for _, subsets in games:
        total += reduce(mul, (
            max(subset.get(color, 0) for subset in subsets)
            for color in 'red,green,blue'.split(',')
        ))
    return total


def parse(line):
    m = re.match(r'Game (\d+): ', line)
    gid = int(m.group(1))
    subsets = []
    for part in line[m.end():].split(';'):
        subset = {}
        for m in re.finditer(r'(\d+) (red|green|blue)', part):
            subset[m.group(2)] = int(m.group(1))
        subsets.append(subset)
    return (gid, subsets)


def test_part1():
    TEXT = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    """.strip()
    games = line_parser(TEXT, parse=parse)
    assert part1(games) == 8


def test_part2():
    TEXT = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    """.strip()
    games = line_parser(TEXT, parse=parse)
    assert part2(games) == 2286


if __name__ == "__main__":
    LINES = line_parser(get_input(day=2, year=2023), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

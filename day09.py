"""Solution to day 9 of Advent of Code"""

from get_input import get_input, line_parser
from functools import reduce


def part1(lines, track=-1, predict=sum):
    total = 0
    for line in lines:
        ends = []
        while not all(n == 0 for n in line):
            ends.append(line[track])
            line = [a-b for a, b in zip(line[1:], line)]
        total += predict(ends)
    return total


def part2(lines):
    def predict(starts):
        return reduce(lambda tot, v: v - tot, reversed(starts), 0)
    return part1(lines, track=0, predict=predict)


def parse(line):
    return [int(n) for n in line.split(' ')]


TEXT = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def test_part1():
    readings = line_parser(TEXT, parse=parse)
    assert part1(readings) == 114


def test_part2():
    readings = line_parser(TEXT, parse=parse)
    assert part2(readings) == 2


if __name__ == "__main__":
    LINES = line_parser(get_input(day=9, year=2023), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

"""Solution to day 8 of Advent of Code"""

from get_input import get_input
from itertools import cycle
import math
import re


def part1(dir_map, start="AAA", end=lambda k: k == "ZZZ"):
    dirs, mapping = dir_map
    pos = start
    for n, d in enumerate(cycle(dirs)):
        if end(pos):
            return n
        pos = mapping[pos][0 if d == 'L' else 1]


def part2(dir_map):
    cycle_times = []
    for pos in (p for p in dir_map[1].keys() if p[-1] == 'A'):
        cycle_times.append(part1(dir_map, start=pos, end=lambda k: k[-1] == 'Z'))
    return math.lcm(*cycle_times)


def parse(text):
    lines = iter(text.splitlines())
    dirs = next(lines)
    assert "" == next(lines)
    mapping = {}
    for line in lines:
        m = re.match(r"(...) = \((...), (...)\)", line)
        mapping[m.group(1)] = (m.group(2), m.group(3))
    return (dirs, mapping)


TEXT = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""


def test_part1():
    dirs = parse(TEXT)
    assert part1(dirs) == 6


TEXT2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


def test_part2():
    dirs = parse(TEXT2)
    assert part2(dirs) == 6


if __name__ == "__main__":
    LINES = parse(get_input(day=8, year=2023))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

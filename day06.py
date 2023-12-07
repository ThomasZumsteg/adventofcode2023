"""Solution to day 6 of Advent of Code"""

from get_input import get_input
import re


def part1(races):
    total = 1
    for time, max_dis in zip(races[0], races[1]):
        total *= sum(1 for t in range(0, time) if (time - t) * t > max_dis)
    return total


def part2(races):
    time = int(''.join(str(n) for n in races[0]))
    distance = int(''.join(str(n) for n in races[1]))
    return int((time*time - 4*distance) ** 0.5)


TEXT = """Time:      7  15   30
Distance:  9  40  200"""


def test_part1():
    games = parse(TEXT)
    assert part1(games) == 288


def test_part2():
    games = parse(TEXT)
    assert part2(games) == 71503


def parse(text):
    times, distances = text.splitlines()
    times = tuple(int(t) for t in re.findall(r'\d+', times))
    distances = tuple(int(d) for d in re.findall(r'\d+', distances))
    return (times, distances)


if __name__ == "__main__":
    LINES = parse(get_input(6, 2023))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

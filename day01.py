"""Solution to day 1 of Advent of Code"""

from get_input import get_input, line_parser


def part1(lines):
    raise NotImplementedError()


def part2(lines):
    raise NotImplementedError()


def parse(text):
    raise NotImplementedError()


def test_part1():
    pass


def test_part2():
    pass


if __name__ == "__main__":
    LINES = line_parser(get_input(day=1, year=2023), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

"""Solution to day 13 of Advent of Code"""

from get_input import get_input, line_parser
from itertools import product


def find_split(rows):
    for m, lines in [(100, rows), (1, list(zip(*rows)))]:
        for split in range(1, len(lines)):
            for up, down in zip(reversed(lines[:split]), lines[split:]):
                if up != down:
                    break
            else:
                yield m * split
    return None


def part1(patterns):
    total = 0
    for pattern in patterns:
        total += next(find_split(pattern))
    return total


def part2(patterns):
    total = 0
    for pattern in patterns:
        assert all(len(line) == len(pattern[0]) for line in pattern)
        old = next(find_split(pattern))
        assert old is not None
        found = False
        for r, c in product(range(0, len(pattern)), range(0, len(pattern[0]))):
            if found:
                break
            copy = list(list(row) for row in pattern)
            copy[r][c] = '.' if copy[r][c] == '#' else '#'
            for split in find_split(copy):
                if split == old:
                    continue
                total += split
                found = True
                break
        else:
            raise NotImplementedError
    return total


TEXT = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


def test_part1():
    patterns = line_parser(TEXT, seperator="\n\n", parse=lambda line: tuple(line.splitlines()))
    assert part1(patterns) == 405


def test_part2():
    patterns = line_parser(TEXT, seperator="\n\n", parse=lambda line: tuple(line.splitlines()))
    assert part2(patterns) == 400


if __name__ == "__main__":
    LINES = line_parser(get_input(day=13, year=2023), seperator="\n\n", parse=lambda line: tuple(line.splitlines()))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

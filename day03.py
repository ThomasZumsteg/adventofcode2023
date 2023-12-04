"""Solution to day 2 of Advent of Code"""

from get_input import get_input, line_parser
from collections import defaultdict
from operator import mul
from functools import reduce


def part1(lines):
    total = 0
    # symbols = defaultdict(set)
    seen = set()
    for l, line in enumerate(lines):
        for c, char in enumerate(line):
            pos = complex(l, c)
            if pos in seen:
                continue
            has_symbol = False
            num = ""
            while char.isdigit():
                seen.add(pos)
                for diff in (-1-1j, -1-0j, -1+1j, -1j, +1j, 1-1j, 1+0j, 1+1j):
                    sur = pos + diff
                    if not (0 <= sur.real < len(lines) and 0 <= sur.imag < len(line)):
                        continue
                    schar = lines[int(sur.real)][int(sur.imag)]
                    if not (schar.isdigit() or schar == '.'):
                        has_symbol = True
                num += char
                pos += 0+1j
                if int(pos.imag) >= len(line):
                    break
                char = line[int(pos.imag)]
            if has_symbol:
                total += int(num)
    return total


def part2(lines):
    total = 0
    gears = defaultdict(set)
    seen = set()
    for l, line in enumerate(lines):
        for c, char in enumerate(line):
            pos = complex(l, c)
            if pos in seen:
                continue
            symbols = []
            num = ""
            while char.isdigit():
                seen.add(pos)
                for diff in (-1-1j, -1-0j, -1+1j, -1j, +1j, 1-1j, 1+0j, 1+1j):
                    sur = pos + diff
                    if not (0 <= sur.real < len(lines) and 0 <= sur.imag < len(line)):
                        continue
                    schar = lines[int(sur.real)][int(sur.imag)]
                    if schar == '*':
                        symbols.append(sur)
                num += char
                pos += 0+1j
                if int(pos.imag) >= len(line):
                    break
                char = line[int(pos.imag)]
            for s in symbols:
                gears[s].add(int(num))
    total = 0
    for vals in gears.values():
        assert len(vals) < 3
        if len(vals) == 2:
            total += reduce(mul, vals)
    return total


def parse(lines):
    result = {}
    for l, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == '.':
                continue
            result[complex(l, c)] = char
    return result


def test_part1():
    TEXT = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
    """
    lines = line_parser(TEXT, parse=list)
    assert part1(lines) == 4361


def test_part2():
    TEXT = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
    """
    lines = line_parser(TEXT, parse=list)
    assert part2(lines) == 467835


if __name__ == "__main__":
    LINES = line_parser(get_input(day=3, year=2023), parse=list)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

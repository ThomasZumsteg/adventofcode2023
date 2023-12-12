"""Solution to day 11 of Advent of Code"""

from get_input import get_input
from collections import defaultdict
from itertools import combinations


def part1(image, gap=2):
    assert set(v for v in image.values()) == set(('#',))

    rows = defaultdict(set)
    for p in image:
        rows[p.real].add(p)
    carry = 0+0j
    for r in range(0, int(max(rows))+1):
        rows[r] = [p+carry for p in rows[r]]
        if len(rows[r]) == 0:
            carry += complex((gap-1), 0)

    cols = defaultdict(set)
    for p in (p for row in rows.values() for p in row):
        cols[p.imag].add(p)
    carry = 0+0j
    for c in range(0, int(max(cols))+1):
        cols[c] = [p+carry for p in cols[c]]
        if len(cols[c]) == 0:
            carry += complex(0, (gap-1))

    galaxies = set(p for col in cols.values() for p in col)
    return sum(
        int(abs(i.real - j.real) + abs(i.imag - j.imag))
        for i, j in combinations(galaxies, 2)
    )


def part2(image, gap=1_000_000):
    return part1(image, gap=gap)


TEXT = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


def mappify(text):
    result = {}
    for r, row in enumerate(text.splitlines()):
        for c, char in enumerate(row):
            if char == '.':
                continue
            result[complex(r, c)] = char
    return result


def test_part1():
    image = mappify(TEXT)
    assert part1(image) == 374


def test_part2():
    image = mappify(TEXT)
    part2(image, gap=0)
    assert part2(image, gap=2) == 374
    part2(image, gap=2)
    assert part2(image, gap=10) == 1030
    assert part2(image, gap=100) == 8410


if __name__ == "__main__":
    LINES = mappify(get_input(day=11, year=2023))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

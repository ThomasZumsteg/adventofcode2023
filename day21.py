"""Solution to day 21 of Advent of Code"""

from get_input import get_input
from collections import defaultdict
import pytest


def part1(rocks, steps=64):
    return part2(rocks, steps=steps)


def part2(rocks, steps=26501365):
    assert rocks.rows == rocks.cols, "Only works for squares"

    rocks = rocks.copy()
    start = next(k for k, v in rocks.items() if v == 'S')
    del rocks[start]

    magic = rocks.rows+1  # Assume pattern is cyclical around the board size
    magic_sequence = []
    magic_check = 2

    positions = {start: set((0+0j,))}
    for n in range(steps):
        if (steps - n) % magic == 0:
            magic_sequence.append(sum(len(vals) for vals in positions.values()))
            offset = 3+magic_check
            if len(magic_sequence) >= offset:
                a, b, c, *ds = magic_sequence[-offset:]
                A, rem = divmod(c - 2*b + a, 2)
                B = c - b - 5*A
                C = a - B - A

                def quad(i):
                    i = (i-n+offset*magic) / magic
                    return A*i**2 + B*i + C

                # print(f"{A}n^2+{B}n+{C}={quad(n)} : {ds[-1]}", rem)
                if rem == 0 and all(quad(n-magic*s) == d for s, d in enumerate(reversed(ds))):
                    return int(quad(steps))
        next_positions = defaultdict(set)
        for diff in (1, -1, 1j, -1j):
            for position, boards in positions.items():
                step = position+diff
                if not rocks.on_map(step):
                    step = complex(step.real % (rocks.rows+1), step.imag % (rocks.cols+1))
                    boards = set(b+diff for b in boards)
                if step not in rocks:
                    next_positions[step].update(boards)
        positions = next_positions
    return sum(len(vals) for vals in positions.values())


TEXT = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""


@pytest.fixture
def items():
    return mappify(TEXT)


def test_part1(items):
    assert part1(items, steps=6) == 16


def test_part2(items):
    assert part2(items, steps=6) == 16
    assert part2(items, steps=10) == 50
    assert part2(items, steps=50) == 1594
    assert part2(items, steps=100) == 6536
    assert part2(items, steps=500) == 167004
    assert part2(items, steps=1000) == 668697
    assert part2(items, steps=5000) == 16733044


def mappify(text):
    result = Map()
    for r, row in enumerate(text.splitlines()):
        for c, char in enumerate(row):
            if char == '.':
                continue
            result[complex(r, c)] = char
    result.cols = c
    result.rows = r
    return result


class Map(dict):
    def __init__(self, *args, rows=None, cols=None, **kwargs):
        self.rows = rows or 0
        self.cols = cols or 0
        super().__init__(*args, **kwargs)
        if len(self.keys()) > 0 and (rows is None or cols is None):
            self.rows = int(max(k.real for k in self.keys()))
            self.cols = int(max(k.imag for k in self.keys()))

    def on_map(self, point):
        return 0 <= point.real <= self.rows and 0 <= point.imag <= self.cols

    def __setitem__(self, key, value):
        val = super().__setitem__(key, value)
        self.rows = max(self.rows, int(key.real))
        self.cols = max(self.cols, int(key.imag))
        assert val is None
        return val

    def __str__(self):
        rows = []
        for r in range(0, self.rows+1):
            row = []
            for c in range(0, self.cols+1):
                row.append(self.get(complex(r, c), '.'))
            rows.append(row)
        return '\n'.join(''.join(row) for row in rows)

    def copy(self):
        return Map(super().copy(), rows=self.rows, cols=self.cols)


if __name__ == "__main__":
    LINES = mappify(get_input(day=21, year=2023))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

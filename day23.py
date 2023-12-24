"""Solution to day 23 of Advent of Code"""

from get_input import get_input
from collections import defaultdict, deque
import pytest


def part1(path):
    dirs = {'<': -1j, '>': 1j, 'v': 1, '^': -1}

    def verify_path(steps):
        for p, q in zip(steps, steps[1:]):
            if path.get(p) == '.':
                continue
            if d := dirs.get(path.get(p)):
                if p - q != d:
                    return False
        return True

    return part2(path, verify_path=verify_path)


def part2(path, verify_path=lambda _: True):
    start = next(complex(0, c) for c in range(0, path.cols+1) if complex(0, c) not in path)
    end = next(complex(path.rows, c) for c in range(0, path.cols+1) if complex(path.rows, c) not in path)
    intersections = defaultdict(dict, {start: {}, end: {}})
    dirs = {'<': -1j, '>': 1j, 'v': 1, '^': -1}
    queue = deque([[start, start+1]])
    while queue:
        *steps, current = queue.pop()
        options = []
        for d in dirs.values():
            step = current + d
            if path.get(step, '.') == '#' or not path.on_map(step):
                continue
            options.append(step)
        if len(options) > 2 or current in intersections:
            assert current not in intersections[steps[0]]
            if verify_path(list(reversed(steps + [current]))):
                intersections[steps[0]][current] = len(steps)
            if current not in intersections:
                queue.extend([current, o] for o in options)
        else:
            options.remove(steps[-1])
            queue.append(steps + [current, options[0]])
    queue = deque([(0, [start])])
    best = 0
    while queue:
        size, (*steps, current) = queue.pop()
        if current == end:
            best = max(size, best)
            continue
        if current in steps:
            continue
        for inter, diff in intersections[current].items():
            queue.append((size + diff, steps + [current, inter]))
    return best


TEXT = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""


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


@pytest.fixture
def items():
    return mappify(TEXT)


def test_part1(items):
    assert part1(items) == 94


def test_part2(items):
    assert part2(items) == 154


if __name__ == "__main__":
    LINES = mappify(get_input(day=23, year=2023))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

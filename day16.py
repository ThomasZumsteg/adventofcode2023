"""Solution to day 16 of Advent of Code"""

from get_input import get_input
import itertools


def part1(mirrors, start=(0+0j, 0+1j)):
    queue = [start]
    seen = set()
    while queue:
        beam = queue.pop()
        if beam in seen or not mirrors.on_map(beam[0]):
            continue
        seen.add(beam)
        match mirrors.get(beam[0]):
            case '/':
                match beam[1]:
                    case 1:
                        dir = -1j
                    case -1:
                        dir = 1j
                    case 1j:
                        dir = -1+0j
                    case -1j:
                        dir = 1+0j
                queue.append((beam[0]+dir, dir))
            case  '\\':
                match beam[1]:
                    case 1:
                        dir = 1j
                    case -1:
                        dir = -1j
                    case 1j:
                        dir = 1+0j
                    case -1j:
                        dir = -1+0j
                queue.append((beam[0]+dir, dir))
            case '|' if beam[1].real == 0:
                queue.append((beam[0]+1+0j, 1+0j))
                queue.append((beam[0]+(-1+0j), -1+0j))
            case '-' if beam[1].imag == 0:
                queue.append((beam[0]+(-1j), -1j))
                queue.append((beam[0]+1j, 1j))
            case _:
                queue.append((beam[0]+beam[1], beam[1]))
    return len(set((p[0] for p in seen)))


def part2(mirrors):
    horiz = ((complex(n, 0), d) for d in (0+1j, 0-1j) for n in range(0, mirrors.rows+1))
    vert = ((complex(0, n), d) for d in (-1+0j, 1+0j) for n in range(0, mirrors.cols+1))
    return max(part1(mirrors, start=start) for start in itertools.chain(horiz, vert))


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
    def __init__(self, *args, **kwargs):
        self.rows = 0
        self.cols = 0
        super().__init__(*args, **kwargs)

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


TEXT = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""


def test_part1():
    mirrors = mappify(TEXT)
    assert part1(mirrors) == 46


def test_part2():
    items = mappify(TEXT)
    assert part2(items) == 51


if __name__ == "__main__":
    LINES = mappify(get_input(day=16, year=2023))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

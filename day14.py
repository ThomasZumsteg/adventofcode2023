"""Solution to day 14 of Advent of Code"""

from get_input import get_input


def cycle(rocks, direction, offset):
    sorter = {
        -1: lambda p: p[0].real,
        1: lambda p: -p[0].real,
        -1j: lambda p: p[0].imag,
        1j: lambda p: -p[0].imag,
    }
    rocks = dict(rocks)
    result = dict()
    for p, char in sorted(rocks.items(), key=sorter[direction]):
        if char == 'O':
            step = direction + p
            while step not in result and offset.imag+1 > step.imag > -1 and offset.real+1 > step.real > -1:
                p = step
                step += direction
        result[p] = char
    return tuple(sorted(result.items(), key=lambda p: (p[0].real, p[0].imag)))


def get_grid(items, size):
    rows = []
    for r in range(0, int(size.real+1)):
        row = []
        for c in range(0, int(size.imag+1)):
            row.append(items.get(complex(r, c), '.'))
        rows.append(row)
    return "\n".join(''.join(row) for row in rows)


def part1(rocks_offset):
    rocks, offset = rocks_offset
    rocks = cycle(rocks, -1, offset)
    return int(sum(1 + offset.real - p.real for p, char in rocks if char == 'O'))


def part2(rocks_offset):
    cycles = 1000000000
    rocks, offset = rocks_offset
    n_rocks = sum(1 for r in rocks.values() if r == 'O')
    rocks = sorted(rocks.items(), key=lambda p: (p[0].real, p[0].imag))
    indexes = {}
    for n in range(cycles):
        for direction in (-1, -1j, 1, 1j):
            rocks = cycle(rocks, direction, offset)
            assert n_rocks == sum(1 for _, r in rocks if r == 'O')
        if index := indexes.get(rocks):
            final = ((cycles - index - 1) % (n - index)) + index
            rocks = next(r for r, i in indexes.items() if i == final)
            break
        indexes[rocks] = n
    return int(sum(1 + offset.real - p.real for p, char in rocks if char == 'O'))


TEXT = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


def parse(text):
    result = {}
    for r, row in enumerate(text.splitlines()):
        for c, char in enumerate(row):
            if char == '.':
                continue
            result[complex(r, c)] = char
    return (result, complex(r, c))


def test_part1():
    rocks = parse(TEXT)
    assert part1(rocks) == 136


def test_part2():
    rocks = parse(TEXT)
    assert part2(rocks) == 64


if __name__ == "__main__":
    LINES = parse(get_input(day=14, year=2023))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

"""Solution to day 18 of Advent of Code"""

from get_input import get_input, line_parser


def part1(steps, column=0):
    area = 1  # Starting point has area 1
    pos = 0+0j
    for heading, dist in map(lambda v: v[column], steps):
        step = pos + heading*dist
        # Shoelace formula plus line "area": https://en.wikipedia.org/wiki/Shoelace_formula
        area += (dist + pos.imag*step.real - pos.real*step.imag) / 2
        pos = step
    return int(abs(area))


def part2(steps):
    return part1(steps, column=1)


TEXT = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""


def test_part1():
    steps = line_parser(TEXT, parse=parse)
    assert part1(steps) == 62


def test_part2():
    steps = line_parser(TEXT, parse=parse)
    assert part2(steps) == 952408144115


def parse(line):
    d, s, h = line.split(' ')
    headings = "RDLU"
    dirs = [0+1j, 1+0j, 0+-1j, -1+0j]
    return ((dirs[headings.index(d)], int(s)), (dirs[int(h[-2])], int(h[2:-2], base=16)))


if __name__ == "__main__":
    LINES = line_parser(get_input(day=18, year=2023), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

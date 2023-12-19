"""Solution to day 1 of Advent of Code"""

from get_input import get_input, line_parser


BASE = {str(n): str(n) for n in range(10)}
EXTRA = {
    **{k: str(n) for n, k in enumerate('one,two,three,four,five,six,seven,eight,nine'.split(','), 1)},
    **BASE,
}


def part1(lines, values=None):
    values = values or BASE
    total = 0
    for line in lines:
        start = min((key for key in values if key in line), key=lambda k: line.find(k))
        end = max((key for key in values if key in line), key=lambda k: line.rfind(k))
        total += int(values[start] + values[end])
    return total


def part2(lines):
    return part1(lines, EXTRA)


TEXT = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""


def test_part1():
    assert part1(line_parser(TEXT, parse=str)) == 142


TEXT2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


def test_part2():
    assert part2(line_parser(TEXT2, parse=str)) == 281


if __name__ == "__main__":
    LINES = line_parser(get_input(day=1, year=2023), parse=str)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

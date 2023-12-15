"""Solution to day 15 of Advent of Code"""

from get_input import get_input, line_parser
from functools import reduce


def elf_hash(string):
    return reduce(lambda h, c: 17*(h+ord(c)) % 256, string, 0)


def part1(fields):
    return sum(elf_hash(f) for f in fields)


def part2(fields):
    boxes = [{} for _ in range(256)]
    for field in fields:
        label, n = (field[:-1], None) if field.endswith('-') else field.split('=')
        box = boxes[elf_hash(label)]
        if n is None:
            box.pop(label, None)
        else:
            box[label] = int(n)

    return sum(
        b * li * lens
        for b, box in enumerate(boxes, 1)
        for li, lens in enumerate(box.values(), 1)
    )


TEXT = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""


def test_part1():
    fields = line_parser(TEXT, seperator=',', parse=str)
    assert part1(fields) == 1320


def test_part2():
    fields = line_parser(TEXT, seperator=',', parse=str)
    assert part2(fields) == 145


if __name__ == "__main__":
    LINES = line_parser(get_input(day=15, year=2023), seperator=',', parse=str)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

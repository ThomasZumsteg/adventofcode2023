"""Solution to day 22 of Advent of Code"""

from get_input import get_input, line_parser
from itertools import product
import pytest


def take_step(blocks):
    field = set(p for block in blocks for p in block)
    assert len(field) == sum(len(block) for block in blocks)
    falling = []
    for block in blocks:
        field -= block
        step = set((x, y, z-1) for x, y, z in block)
        if all(z > 0 for _, _, z in step) and field.isdisjoint(step):
            field.update(step)
            falling.append(step)
        else:
            field.update(block)
            falling.append(block)
    assert len(falling) == len(blocks)
    return falling


def part1(bricks):
    blocks = []
    for start, end in bricks:
        block = set()
        assert all(s <= e for s, e in zip(start, end))
        for cords in product(*(range(s, e+1) for s, e in zip(start, end))):
            block.add(cords)
        blocks.append(block)
    last = None
    falling = blocks.copy()
    while falling != last:
        last, falling = falling, take_step(falling)

    count = 0
    for f in range(len(falling)):
        subset = falling.copy()
        subset.pop(f)
        if take_step(subset) == subset:
            count += 1
    return count


def part2(bricks):
    blocks = []
    for start, end in bricks:
        block = set()
        assert all(s <= e for s, e in zip(start, end))
        for cords in product(*(range(s, e+1) for s, e in zip(start, end))):
            block.add(cords)
        blocks.append(block)
    last = None
    falling = blocks.copy()
    while falling != last:
        last, falling = falling, take_step(falling)

    count = 0
    for f in range(len(falling)):
        subset = falling.copy()
        subset.pop(f)

        last = None
        update = subset.copy()
        while update != last:
            last, update = update, take_step(update)
        count += sum(1 for s, u in zip(subset, update) if s != u)
    return count


TEXT = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""


@pytest.fixture
def bricks():
    return line_parser(TEXT, parse=parse)


def test_part1(bricks):
    assert part1(bricks) == 5


def test_part2(bricks):
    assert part2(bricks) == 7


def parse(line):
    start, end = line.split('~')
    start = tuple(int(n) for n in start.split(','))
    end = tuple(int(n) for n in end.split(','))
    return (start, end)


if __name__ == "__main__":
    LINES = line_parser(get_input(day=22, year=2023), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    # NOT 2153
    print(f"Part 2: {part2(LINES)}")

"""Solution to day 10 of Advent of Code"""

from get_input import get_input


def get_path(pipes):
    path = list(k for k, v in pipes.items() if v == 'S')
    assert len(path) == 1
    for chars, diff in [('|LJ', 1), ('|F7', -1), ('FL-', -1j), ('-7J', 1j)]:
        if pipes.get(path[0] + diff, '.') in chars:
            if len(path) == 1:
                path.append(path[0] + diff)
            else:
                path.insert(0, path[0] + diff)
    assert len(path) == 3

    def step(pos, prev):
        match pipes[pos]:
            case 'L':
                diffs = (-1, 1j)
            case 'J':
                diffs = (-1, -1j)
            case '|':
                diffs = (-1, 1)
            case '-':
                diffs = (-1j, 1j)
            case 'F':
                diffs = (1, 1j)
            case '7':
                diffs = (1, -1j)
            case _:
                raise NotImplementedError
        return pos + diffs[0 if diffs[1] + pos == prev else 1]

    while path[0] != path[-1]:
        path.insert(0, step(path[0], path[1]))
        path.append(step(path[-1], path[-2]))

    return path[:-1]


def part1(pipes):
    path = get_path(pipes)
    assert len(path) % 2 == 0
    return len(path) // 2


def part2(pipes):
    path = get_path(pipes)
    path_set = set(path)
    path.append(path[0])
    lefts = set()
    rights = set()
    for start, end in zip(path, path[1:]):
        diff = start - end
        left = complex(-diff.imag, diff.real)
        right = complex(diff.imag, -diff.real)
        for side, items in [(left, lefts), (right, rights)]:
            for p in (start, end):
                if side + p not in path_set:
                    items.add(p+side)

    for items in (lefts, rights):
        queue = [item + diff for item in items for diff in [1, -1, 1j, -1j]]
        while queue:
            item = queue.pop()
            if item in items:
                continue
            elif item not in pipes:
                items.clear()
                break
            elif item not in path_set:
                items.add(item)
                queue.extend([item+diff for diff in [1, -1, 1j, -1j]])
    return len(rights) + len(lefts)


TEXT = """.....
.S-7.
.|.|.
.L-J.
....."""


TEXT2 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""


TEXT3 = """..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
.........."""


TEXT4 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ... """


TEXT5 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""


def parse(text):
    result = {}
    for r, row in enumerate(text.splitlines()):
        for c, char in enumerate(row):
            result[complex(r, c)] = char
    return result


def test_part1():
    pipes = parse(TEXT)
    assert part1(pipes) == 4
    pipes = parse(TEXT2)
    assert part1(pipes) == 8


def test_part2():
    pipes = parse(TEXT3)
    assert part2(pipes) == 4
    pipes = parse(TEXT4)
    assert part2(pipes) == 8
    pipes = parse(TEXT5)
    assert part2(pipes) == 10


if __name__ == "__main__":
    LINES = parse(get_input(day=10, year=2023))
    print(f"Part 1: {part1(LINES)}")
    # 567 is correct
    print(f"Part 2: {part2(LINES)}")

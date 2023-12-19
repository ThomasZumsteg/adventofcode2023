"""Solution to day 17 of Advent of Code"""

from get_input import get_input
from dataclasses import dataclass, field
import heapq


@dataclass(order=True)
class State:
    loss: int
    position: complex = field(compare=False)
    heading: complex = field(compare=False)
    same: int = field(compare=False)
    path: tuple[complex] = field(compare=False)

    def forward(self):
        return State(self.loss, self.position, self.heading, self.same, self.path)

    def left(self):
        left = complex(-self.heading.imag, -self.heading.real)
        return State(self.loss, self.position, left, 0, self.path)

    def right(self):
        right = complex(self.heading.imag, self.heading.real)
        return State(self.loss, self.position, right, 0, self.path)


def part1(lava, short=0, long=3):
    queue = [State(0, 0+0j, 1+0j, 0, tuple()), State(0, 0+0j, 0+1j, 0, tuple())]
    end = complex(lava.rows, lava.cols)
    seen = set()
    while queue:
        state = heapq.heappop(queue)
        state.path = state.path + (state.position,)
        state.position += state.heading
        state.same += 1
        if state.same > long or not lava.on_map(state.position):
            continue
        state.loss += lava[state.position]
        if state.position == end:
            return state.loss
        if (state.position, state.same, state.heading) in seen:
            continue
        seen.add((state.position, state.same, state.heading))
        heapq.heappush(queue, state.forward())
        if state.same >= short:
            heapq.heappush(queue, state.left())
            heapq.heappush(queue, state.right())
    raise NotImplementedError


def part2(lava):
    return part1(lava, short=4, long=10)


TEXT = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""


def mappify(text):
    result = Map()
    for r, row in enumerate(text.splitlines()):
        for c, char in enumerate(row):
            if char == '.':
                continue
            result[complex(r, c)] = int(char)
    result.cols = c
    result.rows = r
    return result


class Map(dict):
    def __init__(self, *args, **kwargs):
        self.rows = 0
        self.cols = 0
        super().__init__(*args, **kwargs)
        if len(self.keys()) > 0:
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


def test_part1():
    lava = mappify(TEXT)
    assert part1(lava) == 102


def test_part2():
    lava = mappify(TEXT)
    assert part2(lava) == 94


if __name__ == "__main__":
    LINES = mappify(get_input(day=17, year=2023))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

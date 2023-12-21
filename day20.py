"""Solution to day 20 of Advent of Code"""

from get_input import get_input, line_parser
from math import lcm
from itertools import count
from functools import reduce
from collections import defaultdict
import pytest


def part1(modules):
    module_dict = {}
    conjunctions = defaultdict(dict)
    module_dict['output'] = {'type': 'output', 'dest': tuple()}
    for mod_type, name, dest in modules:
        for d in dest:
            conjunctions[d][name] = 0
        module_dict[name] = {'type': mod_type, 'dest': dest}
        match mod_type:
            case '%':
                module_dict[name]['state'] = 0
            case '&':
                module_dict[name]['state'] = conjunctions[name]
    pulses = {1: 0, 0: 0}
    for _ in range(1000):
        queue = [('button', 'broadcaster', 0)]
        while queue:
            src, dest, pulse = queue.pop(0)
            pulses[pulse] += 1
            if dest not in module_dict:
                continue
            module = module_dict[dest]
            match module['type']:
                case 'broadcaster':
                    queue.extend((dest, d, pulse) for d in module['dest'])
                case '&':
                    module['state'][src] = pulse
                    result = 0 if all(v == 1 for v in module['state'].values()) else 1
                    queue.extend((dest, d, result) for d in module['dest'])
                case '%' if pulse == 0:
                    module['state'] = int(not module['state'])
                    queue.extend((dest, d, module['state']) for d in module['dest'])
    return pulses[0] * pulses[1]


def part2(modules):
    module_dict = {}
    conjunctions = defaultdict(dict)
    module_dict['output'] = {'type': 'output', 'dest': tuple()}
    for mod_type, name, dest in modules:
        for d in dest:
            conjunctions[d][name] = 0
        module_dict[name] = {'type': mod_type, 'dest': dest}
        match mod_type:
            case '%':
                module_dict[name]['state'] = 0
            case '&':
                module_dict[name]['state'] = conjunctions[name]
    undertest = {v: [] for v in module_dict['ql']['state']}
    for n in count(1):
        queue = [('button', 'broadcaster', 0)]
        while queue:
            src, dest, pulse = queue.pop(0)
            if dest == 'rx':
                if pulse == 0:
                    return n
                continue
            module = module_dict[dest]
            match module['type']:
                case 'broadcaster':
                    queue.extend((dest, d, pulse) for d in module['dest'])
                case '&':
                    if dest == 'ql' and pulse == 1:
                        undertest[src].append(n)
                    module['state'][src] = pulse
                    result = 0 if all(v == 1 for v in module['state'].values()) else 1
                    queue.extend((dest, d, result) for d in module['dest'])
                case '%' if pulse == 0:
                    module['state'] = int(not module['state'])
                    queue.extend((dest, d, module['state']) for d in module['dest'])
        if all(len(v) >= 2 for v in undertest.values()):
            spacing = []
            for name, vals in undertest.items():
                diffs = []
                for f, s in zip(vals, vals[1:]):
                    diffs.append(s - f)
                assert diffs[0] == vals[0]
                spacing.append(diffs[0])
            return reduce(lcm, spacing, 1)


TEXT = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""


TEXT2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""


def test_part1():
    items = line_parser(TEXT, parse=parse)
    assert part1(items) == 32000000

    items = line_parser(TEXT2, parse=parse)
    assert part1(items) == 11687500


@pytest.mark.skip
def test_part2(items):
    assert part2(items) == 0


def parse(line):
    module, dest = line.split(' -> ')
    if module == 'broadcaster':
        mod_type = module
    else:
        mod_type, module = module[0], module[1:]
    return mod_type, module, tuple(dest.split(', '))


if __name__ == "__main__":
    LINES = line_parser(get_input(day=20, year=2023), parse=parse)
    # Too low: 702294720
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

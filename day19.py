"""Solution to day 19 of Advent of Code"""

from functools import reduce
from get_input import get_input
from operator import lt, gt, mul
import pytest
import re


def part1(workflow_parts):
    workflows, parts = workflow_parts
    total = 0
    for part in parts:
        workflow = 'in'
        steps = iter(workflows[workflow])
        while workflow not in ('A', 'R'):
            step = next(steps)
            if m := re.match(r'(.+)(<|>)(\d+):(.+)', step):
                attr, cmp, val, step = m.groups()
                check = lt if cmp == '<' else gt
            if m is None or check(part[attr], int(val)):
                workflow = step
                steps = iter(workflows.get(step, []))
        if workflow == 'A':
            total += sum(part.values())
        else:
            assert workflow == 'R'
    return total


def part2(workflow_parts):
    workflows = workflow_parts[0]
    acceptable = set()
    queue = [(0, 'in', tuple())]
    max_val = 4000
    while queue:
        s, w, p = queue.pop()
        if w == 'A':
            acceptable.add(p)
            continue
        elif w == 'R':
            continue
        if m := re.match(r'(.+)(<|>)(\d+):(.+)', workflows[w][s]):
            attr, cmp, val, step = m.groups()
            if cmp == '<':
                match, unmatch = (1, int(val)), (int(val), max_val+1)
            elif cmp == '>':
                match, unmatch = (int(val)+1, max_val+1), (1, int(val)+1)
            queue.append((0, step, p+((attr, match),)))
            queue.append((s+1, w, p+((attr, unmatch),)))
        else:
            queue.append((0, workflows[w][s], p))
    total = 0
    for accept in acceptable:
        part = {v: set(range(1, max_val+1)) for v in 'xmas'}
        for attr, rng in accept:
            part[attr].intersection_update(range(*rng))
        total += reduce(mul, (len(v) for v in part.values()), 1)
    return total


TEXT = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""


@pytest.fixture
def items():
    return parse(TEXT)


def test_part1(items):
    assert part1(items) == 19114


def test_part2(items):
    assert part2(items) == 167409079868000


def parse(text):
    workflows = {}
    lines = iter(text.splitlines())
    while (line := next(lines)) != "":
        m = re.match(r'(.+)\{(.+)\}', line)
        workflows[m.group(1)] = list(m.group(2).split(','))
    parts = []
    for line in lines:
        vals = map(lambda f: f.split('='), line.strip('{}').split(','))
        parts.append({i: int(val) for i, val in vals})
    return workflows, parts


if __name__ == "__main__":
    LINES = parse(get_input(day=19, year=2023))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

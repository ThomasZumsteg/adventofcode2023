"""Solution to day 12 of Advent of Code"""

from get_input import get_input, line_parser
from functools import cache


def solutions_iter(template, groups):
    queue = [(template, groups, [])]
    seen = {("", tuple()): 1, ("", (0,)): 1}
    total = 0
    while queue:
        temp, group, traceback = queue.pop()
        if (temp, group) in seen:
            total += seen[(temp, group)]
            for t in traceback:
                assert seen.get(t, seen[(temp, group)]) == seen[(temp, group)]
                seen[t] = seen[(temp, group)]
            continue
        if temp == "":
            for t in traceback:
                assert seen.get(t, 0) == 0
                seen[t] = 0
            continue

        traceback.append((temp, group))
        match temp[0]:
            case '?':
                # asssume '.'
                queue.append(('.' + temp[1:], group, traceback.copy()))
                # asssume '#'
                queue.append(('#' + temp[1:], group, traceback.copy()))
            case '#':
                if len(group) <= 0 or len(temp) < group[0] or '.' in temp[:group[0]] or \
                        (len(temp) > group[0]+1 and temp[group[0]+1] == '#'):
                    for t in traceback:
                        seen[t] = 0
                    continue
                queue.append((temp[group[0]:], group[1:], traceback.copy()))
            case '.':
                queue.append((temp[1:], group, traceback.copy()))
            case _:
                raise NotImplementedError
    # print(f"{template} {groups} {len(ways)}")
    return total


@cache
def solutions(template, counts):
    if template == "":
        if counts == tuple() or counts == (0, ):
            return 1
        return 0
    match template[0]:
        case '?':
            return solutions('#' + template[1:], counts) + solutions('.' + template[1:], counts)
        case '#':
            if len(counts) <= 0 or counts[0] <= 0:
                return 0
            counts = list(counts)
            counts[0] -= 1
            if counts[0] == 0:
                if template.startswith('##'):
                    return 0
                elif template.startswith('#?'):
                    template = "#." + template[2:]
                assert template[:2] == "#." or template == '#'
                counts.pop(0)
            else:
                assert counts[0] > 0
                if template.startswith('#.'):
                    return 0
                elif template.startswith('#?'):
                    template = "##" + template[2:]
            return solutions(template[1:], tuple(counts))
        case '.':
            return solutions(template[1:], tuple(counts))
    raise NotImplementedError


def part1(springs):
    total = 0
    for template, counts in springs:
        total += solutions_iter(template, counts)
    return total


def part2(springs):
    total = 0
    for template, counts in springs:
        template = '?'.join(template for _ in range(5))
        total += solutions(template, counts * 5)
    return total


TEXT = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""


def test_part1():
    springs = line_parser(TEXT, parse=parse)
    assert part1(springs) == 21


def test_part2():
    springs = line_parser(TEXT, parse=parse)
    assert part2(springs) == 525152


def parse(line):
    springs, counts = line.split(' ')
    return (springs, tuple(int(n) for n in counts.split(',')))


if __name__ == "__main__":
    LINES = line_parser(get_input(day=12, year=2023), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

"""Solution to day 5 of Advent of Code"""

from get_input import get_input


def part1(seeds_and_mapping):
    seeds, mapping = seeds_and_mapping
    locations = []
    for seed in seeds:
        prop = 'seed'
        while prop in mapping:
            prop, rngs = mapping[prop]
            for (dest, src, rng) in rngs:
                if src <= seed <= src + rng:
                    seed = seed - src + dest
                    break
        locations.append(seed)
    return min(locations)


def part2(seeds_and_mapping):
    seeds, mapping = seeds_and_mapping
    ranges = list((start, start+length) for start, length in zip(seeds[0::2], seeds[1::2]))
    prop = 'seed'
    while prop in mapping:
        prop, rngs = mapping[prop]
        next_range = []
        for (start, end) in ranges:
            done = False
            while not done:
                for (dest, src, rng) in sorted(rngs, key=lambda k: (k[1], k[1] + k[2])):
                    if src <= start <= src+rng:
                        if src+rng < end:
                            next_range.append((start-src+dest, dest+rng))
                            start = src + rng
                        else:
                            next_range.append((start-src+dest, end-src+dest))
                            done = True
                            break
                else:
                    next_range.append((start, end))
                    done = True
        ranges = next_range
    return min(v for rs in ranges for v in rs)


TEXT = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def test_part1():
    lines = parse(TEXT)
    assert part1(lines) == 35


def test_part2():
    lines = parse(TEXT)
    assert part2(lines) == 46


def parse(text):
    lines = iter(text.splitlines())
    seeds = tuple(int(n) for n in next(lines).split(': ')[1].split(' '))
    mapping = {}
    assert next(lines) == ""
    for line in lines:
        source, to, destination = line.split(' ')[0].split('-')
        assert to == 'to'
        mapp = []
        for line in lines:
            if line == "":
                break
            mapp.append(tuple(int(n) for n in line.split(' ')))
        mapping[source] = (destination, sorted(mapp, key=lambda k: (k[1], k[1] + k[2])))
    return (seeds, mapping)


if __name__ == "__main__":
    LINES = parse(get_input(5, 2023))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")

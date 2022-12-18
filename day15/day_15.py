from pathlib import Path
from dataclasses import dataclass
from functools import cached_property
import re


@dataclass
class Pair:
    sensor: tuple[int, int]
    beacon: tuple[int, int]

    @cached_property
    def distance(self):
        return manhattan_distance(self.sensor, self.beacon)


def manhattan_distance(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(abs(left - right) for left, right in zip(a, b))


def union(*intervals: tuple[int, int]) -> list[tuple[int, int]]:
    intervals = sorted(intervals)
    union = []
    for el in intervals:
        start, end = el
        if len(union) and union[-1][1] >= start - 1:
            union[-1] = (union[-1][0], max(union[-1][1], end))
        else:
            union.append((start, end))
    return union


def scan_row(pairs: list[Pair], row_num: int) -> list[tuple[int, int]]:
    intervals = []
    for pair in pairs:
        delta = abs(pair.sensor[1] - row_num)
        if delta < pair.distance:
            sensor_aff = pair.distance - delta
            interval = (pair.sensor[0] - sensor_aff, pair.sensor[0] + sensor_aff)
            intervals.append(interval)
    intervals = union(*intervals)
    return intervals


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt") as fp:
        lines = fp.read().splitlines()

    pairs: list[Pair] = []
    for line in lines:
        ints = list(map(int, re.findall("-?\d+", line)))
        pairs.append(Pair((ints[0], ints[1]), (ints[2], ints[3])))

    # part 1
    row_num = 10
    intervals = scan_row(pairs, row_num)
    count = sum(interval[1] - interval[0] for interval in intervals)
    print(f"{count=}")

    # part 2
    max_col, max_row = 4000000, 4000000
    for row in range(max_row):
        intervals = scan_row(pairs, row)
        if len(intervals) == 2 and intervals[1][0] < max_row:
            x = intervals[1][0] - 1
            break
    tuning_frequency = x * 4000000 + row
    print(f"{tuning_frequency=}")

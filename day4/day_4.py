from pathlib import Path
from typing import Tuple


def closed_interval_intersection(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    if b[0] < a[0]:
        a, b = b, a
    return max(min(a[1], b[1]) - max(a[0], b[0]) + 1, 0)


def len_closed_interval(a: Tuple[int, int]) -> int:
    return a[1] - a[0] + 1


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt") as fp:
        lines = fp.read().splitlines()

    # part 1
    num_full_inclusion = 0
    for line in lines:
        elf_1, elf_2 = map(lambda x: x.split("-"), line.split(","))
        elf_1 = tuple(map(int, elf_1))
        elf_2 = tuple(map(int, elf_2))
        intersection = closed_interval_intersection(elf_1, elf_2)
        if intersection == len_closed_interval(
            elf_1
        ) or intersection == len_closed_interval(elf_2):
            num_full_inclusion += 1
    print(f"{num_full_inclusion=}")

    # part 2
    num_overlap = 0
    for line in lines:
        elf_1, elf_2 = map(lambda x: x.split("-"), line.split(","))
        elf_1 = tuple(map(int, elf_1))
        elf_2 = tuple(map(int, elf_2))
        intersection = closed_interval_intersection(elf_1, elf_2)
        if intersection:
            num_overlap += 1
    print(f"{num_overlap=}")

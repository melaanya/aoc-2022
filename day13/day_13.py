import functools
from pathlib import Path
from typing import Optional


def compare_pair(left, right) -> Optional[bool]:
    if left == right:
        return 0
    if isinstance(left, list) and isinstance(right, list):
        if not len(right):
            return -1
        elif not len(left):
            return 1
        compare = compare_pair(left[0], right[0])
        return compare_pair(left[1:], right[1:]) if not compare else compare
    elif isinstance(left, list) and isinstance(right, int):
        return compare_pair(left, [right])
    elif isinstance(left, int) and isinstance(right, list):
        return compare_pair([left], right)
    return -1 if right < left else 1


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt") as fp:
        pairs = fp.read().split("\n\n")

    # part 1
    sum_inds = 0
    packets = []
    for ind, pair in enumerate(pairs):
        left, right = list(map(eval, pair.split("\n")))
        packets.extend([left, right])
        is_correct = compare_pair(left, right)
        if is_correct == 1:
            sum_inds += ind + 1
    print(f"{sum_inds=}")

    # part 2
    packets.extend([[[2]], [[6]]])
    packets = sorted(packets, key=functools.cmp_to_key(compare_pair))[::-1]
    ind_first = packets.index([[2]]) + 1
    ind_last = packets.index([[6]]) + 1
    print(f"{ind_first * ind_last=}")

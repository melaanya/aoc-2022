from pathlib import Path


def compute_priority(item: str):
    if item.isupper():
        return ord(item) - 38
    else:
        return ord(item) - 96


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt") as fp:
        rucksacks = fp.read().splitlines()

    # part 1
    priorities = []
    for rucksack in rucksacks:
        first_compartment, second_compartment = (
            set(rucksack[: len(rucksack) // 2]),
            set(rucksack[len(rucksack) // 2 :]),
        )
        intersection = first_compartment.intersection(second_compartment)
        assert len(intersection) == 1

        item = intersection.pop()
        priorities.append(compute_priority(item))

    print(f"{sum(priorities)=}")

    # part 2
    priorities = []
    group_size = 3
    for ind in range(0, len(rucksacks), group_size):
        group = rucksacks[ind : ind + group_size]

        intersection = set.intersection(*map(set, group))
        assert len(intersection) == 1, f"{intersection=}, {len(priorities)=}"

        item = intersection.pop()
        priorities.append(compute_priority(item))

    print(f"{sum(priorities)=}")

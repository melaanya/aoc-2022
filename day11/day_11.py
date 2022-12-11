from dataclasses import dataclass
from functools import reduce
import operator
from pathlib import Path
from typing import Callable


ops = {"+": operator.add, "*": operator.mul}


@dataclass
class Monkey:
    items: list[int]
    operation: Callable
    divisible_by: int
    throw_true: int
    throw_false: int
    count: int = 0

    def __repr__(self):
        return self.items.__repr__()


def parse_data(input: str) -> list[Monkey]:
    monkeys = []
    for monkey_data in input.split("\n\n"):
        lines = monkey_data.split("\n")

        starting_items = list(map(int, lines[1].split(":")[1].split(",")))
        op, by = lines[2].split("old ", 1)[1].split(" ")
        if by == "old":
            fun = lambda x, op=op: ops[op](x, x)
        else:
            fun = lambda x, op=op, by=by: ops[op](x, int(by))
        divisible_by = int(lines[3].rsplit(" ", 1)[-1])
        throw_true = int(lines[4].rsplit(" ", 1)[-1])
        throw_false = int(lines[5].rsplit(" ", 1)[-1])

        cur_monkey = Monkey(starting_items, fun, divisible_by, throw_true, throw_false)
        monkeys.append(cur_monkey)
    return monkeys


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt") as fp:
        input = fp.read()

    monkeys = parse_data(input)

    # part 1
    NUM_ROUNDS = 20
    for round_ in range(NUM_ROUNDS):
        for monkey in monkeys:
            for item in monkey.items:
                item = monkey.operation(item) // 3
                if item % monkey.divisible_by:
                    monkey_recipient = monkey.throw_false
                else:
                    monkey_recipient = monkey.throw_true
                monkeys[monkey_recipient].items.append(item)
            monkey.count += len(monkey.items)
            monkey.items = []

    monkeys_sorted = sorted(monkeys, key=lambda x: x.count)
    busiest = monkeys_sorted[-2:]
    business_level = busiest[0].count * busiest[1].count
    print(f"{business_level=}")

    # part 2
    monkeys = parse_data(input)
    NUM_ROUNDS = 10000

    divisibles = [monkey.divisible_by for monkey in monkeys]
    mod = reduce(operator.mul, divisibles, 1)
    for round_ in range(NUM_ROUNDS):
        for monkey in monkeys:
            for item in monkey.items:
                item = monkey.operation(item) % mod
                if item % monkey.divisible_by:
                    monkey_recipient = monkey.throw_false
                else:
                    monkey_recipient = monkey.throw_true
                monkeys[monkey_recipient].items.append(item)
            monkey.count += len(monkey.items)
            monkey.items = []

    monkeys_sorted = sorted(monkeys, key=lambda x: x.count)
    busiest = monkeys_sorted[-2:]
    business_level = busiest[0].count * busiest[1].count
    print(f"{business_level=}")

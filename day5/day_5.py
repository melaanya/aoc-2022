from pathlib import Path
from collections import defaultdict
import re


def parse_stacks(lines: str) -> dict[int, list[str]]:
    res_stacks = defaultdict(list)
    for line in lines[-2::-1]:
        ind = 1
        while ind < len(line):
            if line[ind] != " ":
                res_stacks[ind // 4 + 1].append(line[ind])
            ind += 4
    return res_stacks


def form_string(stacks: dict[int, list[str]]) -> str:
    result_str = ""
    for stack_ind in sorted(stacks):
        if len(stacks[stack_ind]):
            result_str += stacks[stack_ind].pop()
    return result_str


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt") as fp:
        lines = fp.read()

    orig_stacks, commands = map(lambda x: x.split("\n"), lines.split("\n\n"))

    # part 1
    parsed_stacks = parse_stacks(orig_stacks)
    for command in commands:
        to_move, ind_from, ind_to = map(int, re.findall(r"\d+", command))
        for _ in range(to_move):
            stack_from = parsed_stacks[ind_from]
            stack_to = parsed_stacks[ind_to]
            if len(stack_from):
                el = stack_from.pop()
                stack_to.append(el)

    result_str = form_string(parsed_stacks)
    print(f"{result_str=}")

    # part 2
    parsed_stacks = parse_stacks(orig_stacks)
    for command in commands:
        to_move, ind_from, ind_to = map(int, re.findall(r"\d+", command))

        stack_from = parsed_stacks[ind_from]
        stack_to = parsed_stacks[ind_to]

        stack_to.extend(stack_from[-to_move:])
        parsed_stacks[ind_from] = stack_from[:-to_move]

    result_str = form_string(parsed_stacks)
    print(f"{result_str=}")

from __future__ import annotations
from functools import cached_property
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Union


@dataclass
class File:
    name: str
    size: int


@dataclass
class Dir:
    name: str
    parent: Optional[Dir]
    content: dict[str, Union[File, Dir]] = field(default_factory=dict)

    @cached_property
    def size(self) -> int:
        return sum(obj.size for obj in self.content.values())


def get_sum_small_dir_sizes(node: Dir, SIZE_SMALL: int = 100000) -> int:
    sum_small = 0
    for child in node.content.values():
        if isinstance(child, File):
            continue
        if child.size < SIZE_SMALL:
            sum_small += child.size
        sum_small += get_sum_small_dir_sizes(child, SIZE_SMALL)
    return sum_small


def get_smallest_to_delete(node: Dir, space_needed: int, min_size: int) -> int:
    for child in node.content.values():
        if isinstance(child, File):
            continue
        if child.size > space_needed:
            min_size = min(child.size, min_size)
        min_size = min(min_size, get_smallest_to_delete(child, space_needed, min_size))
    return min_size


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt") as fp:
        lines = fp.read().splitlines()

    root = Dir(name="/", parent=None)
    for line in lines:
        if line.startswith("$"):
            command = line.split(" ", 1)[1]
            if command.startswith("cd"):
                command, where = command.split(" ")
                if where == "..":
                    cur_dir = cur_dir.parent
                elif where == "/":
                    cur_dir = root
                else:
                    cur_dir = cur_dir.content.get(where)
                    if cur_dir is None:
                        raise ValueError(f"Unknown {where}")

        elif line.startswith("dir"):
            name = line.split(" ")[1]
            new_dir = Dir(name=name, parent=cur_dir)
            cur_dir.content[name] = new_dir
        else:
            size, name = line.split(" ")
            new_file = File(name=name, size=int(size))
            cur_dir.content[name] = new_file

    # part 1
    sum_small = get_sum_small_dir_sizes(root)
    print(f"{sum_small=}")

    # part 2
    TOTAL_SPACE = 70000000
    SPACE_NEEDED = 30000000
    free_space = TOTAL_SPACE - root.size
    space_to_free = SPACE_NEEDED - free_space

    min_to_delete = get_smallest_to_delete(root, space_to_free, root.size)
    print(f"{min_to_delete=}")

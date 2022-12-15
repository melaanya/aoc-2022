from copy import deepcopy
from pathlib import Path


def get_ind(position: tuple[int, int], mul: int):
    i, j = position
    return i * mul + j


def put_sand(matrix: list[str], shape: tuple[int, int], start: tuple[int, int]) -> bool:
    width, height = shape
    while matrix[get_ind(start, height)] == "." and start[1] <= height:
        for next in [
            (start[0], start[1] + 1),
            (start[0] - 1, start[1] + 1),
            (start[0] + 1, start[1] + 1),
        ]:
            next_ind = get_ind(next, height)
            if next_ind <= width * height and matrix[get_ind(next, height)] == ".":
                start = next
                break
        else:
            matrix[get_ind(start, height)] = "0"
            return True
    if start[1] <= height:
        return False


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt") as fp:
        paths = fp.read().split("\n")

    max_x, max_y = 0, 0
    paths_processed = []
    for path in paths:
        pairs = path.split(" -> ")
        cur_path = []
        for pair in pairs:
            x, y = map(int, pair.split(","))
            max_x = max(x, max_x)
            max_y = max(y, max_y)
            cur_path.append((x, y))
        paths_processed.append(cur_path)

    width, height = max_x + 1001, max_y + 3
    matrix = ["." for _ in range(width * height)]

    for paths in paths_processed:
        for (x, y), (x_next, y_next) in zip(paths[:-1], paths[1:]):
            if x == x_next:
                step = -1 if y_next < y else 1
                for cur_y in range(y, y_next + step, step):
                    matrix[get_ind((x, cur_y), height)] = "#"
            elif y == y_next:
                step = -1 if x_next < x else 1
                for cur_x in range(x, x_next + step, step):
                    matrix[get_ind((cur_x, y), height)] = "#"
            else:
                raise ValueError("No diagonal lines allowed")

    # part 1
    count = 0
    fill_first = deepcopy(matrix)
    while put_sand(fill_first, (width, height), (500, 0)):
        count += 1
    print(f"{count=}")

    # part 2
    for i in range(width):
        matrix[get_ind((i, height - 1), height)] = "#"

    count = 0
    fill_second = deepcopy(matrix)
    while put_sand(fill_second, (width, height), (500, 0)):
        count += 1
    print(f"{count=}")

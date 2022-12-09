from pathlib import Path


def sign(x: int) -> int:
    if not x:
        return 0
    elif x > 0:
        return 1
    else:
        return -1


def get_h_t_distance(h: list[int, int], t: list[int, int]) -> tuple[int, bool]:
    horizontal_distance = abs(h[0] - t[0])
    vertical_distance = abs(h[1] - t[1])
    return max(horizontal_distance, vertical_distance)


def recompute_t_pos(h: list[int, int], t: list[int, int]) -> list[int, int]:
    distance = get_h_t_distance(h, t)
    if distance > 1:
        t[0] += sign(h[0] - t[0])
        t[1] += sign(h[1] - t[1])
    return t


DIRECTION_MAP = {"R": (1, 1), "L": (1, -1), "U": (0, 1), "D": (0, -1)}

if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt") as fp:
        commands = fp.read().splitlines()

    # part 1
    h_pos, t_pos = [0, 0], [0, 0]
    t_positions = set()
    for command in commands:
        direction, count = command.split(" ")
        where, by = DIRECTION_MAP[direction]
        for _ in range(int(count)):
            h_pos[where] += by
            t_pos = recompute_t_pos(h_pos, t_pos)
            t_positions.add(tuple(t_pos))

    num_unique_positions = len(t_positions)
    print(f"{num_unique_positions=}")

    # part 2
    num_nodes = 10
    positions_last = set()
    rope_nodes = [[0, 0] for _ in range(num_nodes)]
    for command in commands:
        direction, count = command.split(" ")
        where, by = DIRECTION_MAP[direction]
        for _ in range(int(count)):
            rope_nodes[0][where] += by
            for ind in range(1, num_nodes):
                rope_nodes[ind] = recompute_t_pos(rope_nodes[ind - 1], rope_nodes[ind])
            positions_last.add(tuple(rope_nodes[-1]))

    num_unique_positions = len(positions_last)
    print(f"{num_unique_positions=}")

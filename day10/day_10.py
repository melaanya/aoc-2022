from pathlib import Path

CRT_WIDTH = 40


def check_value(cycle: int, x: int, sum_signal: int) -> int:
    if cycle % CRT_WIDTH == 20:
        sum_signal += x * cycle
    return sum_signal


def add_symbol(cycle: int, x: int, crt: str) -> str:
    cycle = (cycle - 1) % CRT_WIDTH
    if x - 1 <= cycle <= x + 1:
        crt += "#"
    else:
        crt += "."
    return crt


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt") as fp:
        commands = fp.read().splitlines()

    # part 1
    cycle, x, sum_signal = 0, 1, 0
    for command in commands:
        if command == "noop":
            cycle += 1
            sum_signal = check_value(cycle, x, sum_signal)
        else:
            command, value = command.split(" ")
            value = int(value)
            for _ in range(2):
                cycle += 1
                sum_signal = check_value(cycle, x, sum_signal)
            x += value

    print(f"{sum_signal=}")

    # part 2
    crt = ""
    cycle, x = 0, 1
    for command in commands:
        if command == "noop":
            cycle += 1
            crt = add_symbol(cycle, x, crt)
        else:
            command, value = command.split(" ")
            value = int(value)
            for _ in range(2):
                cycle += 1
                crt = add_symbol(cycle, x, crt)
            x += value

    crt_strs = [crt[ind : ind + CRT_WIDTH] for ind in range(0, len(crt), CRT_WIDTH)]
    for str_ in crt_strs:
        print(str_ + "\n")

from pathlib import Path

if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt") as fp:
        input = fp.read()

    # part 1
    marker_size, marker_start = 4, -1
    for ind in range(len(input)):
        substr = input[ind : ind + marker_size]
        if len(substr) == len(set(substr)):
            marker_start = ind + marker_size
            break

    print(f"{marker_start=}")

    # part 2
    message_size, message_start = 14, -1
    for ind in range(len(input[marker_start:])):
        substr = input[ind + marker_start : ind + marker_start + message_size]
        if len(substr) == len(set(substr)):
            message_start = ind + marker_start + message_size
            break

    print(f"{message_start=}")

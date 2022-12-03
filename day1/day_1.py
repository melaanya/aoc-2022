from pathlib import Path


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt") as fp:
        lines = fp.read()

    groups = lines.split("\n\n")

    # part one
    calories = [sum(map(int, group.split("\n"))) for group in groups]
    max_calories = max(calories)
    print(f"{max_calories=}")

    # part two
    top_3 = sorted(calories, reverse=True)[:3]
    print(f"{sum(top_3)=}")

    
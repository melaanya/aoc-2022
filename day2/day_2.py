from pathlib import Path

response_to_score = {"X": 1, "Y": 2, "Z": 3}

opponent_response_to_score = {
    ("A", "X"): 3,
    ("A", "Y"): 6,
    ("A", "Z"): 0,
    ("B", "X"): 0,
    ("B", "Y"): 3,
    ("B", "Z"): 6,
    ("C", "X"): 6,
    ("C", "Y"): 0,
    ("C", "Z"): 3,
}

opponent_to_lose = {"A": "Z", "B": "X", "C": "Y"}
opponent_to_win = {"A": "Y", "B": "Z", "C": "X"}


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt") as fp:
        lines = fp.readlines()

    # part 1
    score = 0
    for line in lines:
        opponent, response = line.strip().split(" ")
        score += response_to_score[response]
        score += opponent_response_to_score[(opponent, response)]

    print(f"{score=}")

    # part 2
    score = 0
    for line in lines:
        opponent, advice = line.strip().split(" ")
        if advice == "X":  # we need to lose
            response = opponent_to_lose[opponent]
        elif advice == "Y":  # we need to have a draw
            response = chr(ord(opponent) + 23)
        else:  # we need to win
            response = opponent_to_win[opponent]

        score += response_to_score[response]
        score += opponent_response_to_score[(opponent, response)]

    print(f"{score=}")

from pathlib import Path


def compute_view_distance(el: int, slice: list[int]) -> int:
    distance = 0
    for tree in slice:
        distance += 1
        if tree >= el:
            break
    return distance


if __name__ == "__main__":
    with open(Path(__file__).parent / "data.txt") as fp:
        data = fp.read()

    matrix = [[int(char) for char in line] for line in data.splitlines()]
    matrix_transposed = list(map(list, zip(*matrix)))

    # part 1
    num_visible = 0
    for row_ind, row in enumerate(matrix):
        for col_ind, el in enumerate(row):
            left_slice = row[:col_ind]
            right_slice = row[col_ind + 1 :]

            column = matrix_transposed[col_ind]
            top_slice = column[:row_ind]
            bottom_slice = column[row_ind + 1 :]

            for slice in [left_slice, right_slice, top_slice, bottom_slice]:
                if not len(slice) or el > max(slice):
                    num_visible += 1
                    break

    print(f"{num_visible=}")

    # part 2
    best_scenic_score = -1
    for row_ind, row in enumerate(matrix[1:-1]):
        row_ind += 1
        for col_ind, el in enumerate(row[1:-1]):
            col_ind += 1

            left_slice = row[:col_ind][::-1]
            right_slice = row[col_ind + 1 :]

            column = matrix_transposed[col_ind]
            top_slice = column[:row_ind][::-1]
            bottom_slice = column[row_ind + 1 :]

            scenic_score = 1
            for slice in [left_slice, right_slice, top_slice, bottom_slice]:
                scenic_score *= compute_view_distance(el, slice)
            if scenic_score > best_scenic_score:
                best_scenic_score = scenic_score

    print(f"{best_scenic_score=}")

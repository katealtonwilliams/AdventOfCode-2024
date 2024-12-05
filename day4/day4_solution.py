import numpy as np
from copy import deepcopy


def read_in_input(input_file: str) -> np.ndarray:
    with open(input_file) as raw_word_search:
        return np.array([[*line.strip()] for line in raw_word_search.readlines()])


def found_diagonal_xmas(
    x_coord: tuple[int], direction: tuple[int], word_search: np.ndarray
) -> bool:
    max_row, max_col = word_search.shape
    letters = ["M", "A", "S"]
    current_coord = x_coord
    for letter in letters:
        current_coord = (
            current_coord[0] + direction[0],
            current_coord[1] + direction[1],
        )
        if current_coord[0] < 0 or current_coord[0] > max_row - 1:
            return False
        if current_coord[1] < 0 or current_coord[1] > max_col - 1:
            return False
        if word_search[current_coord] != letter:
            return False
    return True


def find_all_xmas_p1(input_file: str):
    word_search = read_in_input(input_file)
    xmas_count = 0
    for horizontal_line in word_search:
        line = "".join(horizontal_line)
        xmas_count += line.count("XMAS")
        xmas_count += line[::-1].count("XMAS")
    for vertical_line in word_search.T:
        line = "".join(vertical_line)
        xmas_count += line.count("XMAS")
        xmas_count += line[::-1].count("XMAS")
    diagonal_vectors = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
    for row, horizontal_line in enumerate(word_search):
        start_indices = np.where(horizontal_line == "X")[0]
        for start_index in start_indices:
            for vector in diagonal_vectors:
                if found_diagonal_xmas((row, start_index), vector, word_search):
                    xmas_count += 1
    return xmas_count


def get_all_x_mas_combs():
    possible_top_bottom_rows = [
        ["M", ".", "S"],
        ["S", ".", "S"],
        ["M", ".", "M"],
        ["S", ".", "M"],
    ]
    middle_row = [".", "A", "."]
    return (
        np.array(
            [possible_top_bottom_rows[0], middle_row, possible_top_bottom_rows[0]]
        ),
        np.array(
            [possible_top_bottom_rows[2], middle_row, possible_top_bottom_rows[1]]
        ),
        np.array(
            [possible_top_bottom_rows[1], middle_row, possible_top_bottom_rows[2]]
        ),
        np.array(
            [possible_top_bottom_rows[3], middle_row, possible_top_bottom_rows[3]]
        ),
    )


def find_all_x_mas_p2(input_file: str):
    word_search = read_in_input(input_file)
    xmas_combs = get_all_x_mas_combs()
    print(get_all_x_mas_combs())
    xmas_count = 0
    for row_index, row in enumerate(word_search[:-2]):
        for col_index, _ in enumerate(row[:-2]):
            window = deepcopy(
                word_search[row_index : row_index + 3, col_index : col_index + 3]
            )
            window[0, 1] = "."
            window[1, 0] = "."
            window[1, 2] = "."
            window[2, 1] = "."
            for comb in xmas_combs:
                if np.all(comb == window):
                    xmas_count += 1
    return xmas_count


if __name__ == "__main__":
    print(find_all_xmas_p1("day4/day4_final_input.txt"))
    print(find_all_x_mas_p2("day4/day4_final_input.txt"))

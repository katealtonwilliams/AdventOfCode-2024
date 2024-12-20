import numpy as np


def read_in_racetrack(input_file: str) -> np.ndarray:
    with open(input_file) as raw_racetrack:
        return np.array([[*line.strip()] for line in raw_racetrack.readlines()])


DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def find_original_path(racetrack: np.ndarray) -> list[tuple[int, tuple]]:
    start_point = (np.where(racetrack == "S")[0][0], np.where(racetrack == "S")[1][0])
    path = [(0, start_point)]
    seen_points = {start_point}
    while True:
        current_steps, current_point = path[-1]
        for direction in DIRECTIONS:
            next_point = (
                current_point[0] + direction[0],
                current_point[1] + direction[1],
            )
            if next_point not in seen_points:
                seen_points.add(next_point)
                if racetrack[next_point] == "E":
                    return path + [(current_steps + 1, next_point)]
                if racetrack[next_point] != "#":
                    path.append((current_steps + 1, next_point))
                    continue


def is_pos_in_grid(pos: tuple[int], grid: np.ndarray) -> bool:
    row, column = pos
    max_row, max_column = grid.shape
    if row < 0 or column < 0 or row > max_row - 1 or column > max_column - 1:
        return False
    return True


def get_cheat_points(current_point: tuple[int], distance: int) -> list[tuple[int]]:
    points_in_range = []
    for i in range(-distance, distance + 1):
        for j in range(-distance, distance + 1):
            if (m_dist := abs(i) + abs(j)) <= distance:
                point = (current_point[0] + i, current_point[1] + j)
                points_in_range.append((m_dist, point))
    return points_in_range


def find_shortcuts(input_file: str, cheat_distance: int) -> int:
    racetrack = read_in_racetrack(input_file)
    original_path = find_original_path(racetrack)
    path_length_map = {coord: steps for steps, coord in original_path}
    cheats_found = 0
    for _, current_point in original_path:
        for steps_taken, cheat_point in get_cheat_points(current_point, cheat_distance):
            if (
                is_pos_in_grid(cheat_point, racetrack)
                and cheat_point in path_length_map
            ):
                time_saved = (path_length_map[cheat_point]) - (
                    path_length_map[current_point] + steps_taken
                )
                if time_saved >= 100:
                    cheats_found += 1
    return cheats_found


if __name__ == "__main__":
    print(find_shortcuts("day20/day20_final_input.txt", 2))
    print(find_shortcuts("day20/day20_final_input.txt", 20))

import re
import numpy as np


def read_in_robots(input_file: str) -> list[dict[str : tuple[int]]]:
    digit_regex = r"(-?\d+),(-?\d+)"
    all_robots = []
    with open(input_file) as raw_robots:
        for robot in raw_robots.readlines():
            position_and_velocity = {}
            raw_position_and_velocity = re.findall(digit_regex, robot)
            position_and_velocity["position"] = tuple(
                map(int, raw_position_and_velocity[0])
            )
            position_and_velocity["velocity"] = tuple(
                map(int, raw_position_and_velocity[1])
            )
            all_robots.append(position_and_velocity)
    return all_robots


def get_final_position(
    robot: dict[str : tuple[int]], width: int, height: int, seconds: int
) -> tuple[int]:
    x_start, y_start = robot["position"]
    x_velocity, y_velocity = robot["velocity"]
    final_x = (x_start + (x_velocity * seconds)) % width
    final_y = (y_start + (y_velocity * seconds)) % height
    return final_x, final_y


def get_quadrant(
    final_x: int, final_y: int, middle_x: int, middle_y: int
) -> int | None:
    if final_x < middle_x:
        if final_y < middle_y:
            return 1
        if final_y > middle_y:
            return 3
    if final_x > middle_x:
        if final_y < middle_y:
            return 2
        if final_y > middle_y:
            return 4
    return None


def calculate_safety_factor_p1(
    input_file: str, width: int = 101, height: int = 103, seconds: int = 100
) -> int:
    robots = read_in_robots(input_file)
    middle_x = width // 2
    middle_y = height // 2
    quadrants = {1: 0, 2: 0, 3: 0, 4: 0}
    for robot in robots:
        final_x, final_y = get_final_position(robot, width, height, seconds)
        if (quadrant := get_quadrant(final_x, final_y, middle_x, middle_y)) is not None:
            quadrants[quadrant] += 1
    safety_factor = 1
    for robot_count in quadrants.values():
        safety_factor *= robot_count
    return safety_factor


def plot_grid_for_one_time(
    robots: dict[str : tuple[int]], seconds: int, width: int = 101, height: int = 103
) -> np.ndarray:
    grid = np.full((height, width), " ")
    for robot in robots:
        x, y = get_final_position(robot, width, height, seconds)
        grid[y, x] = "#"
    return grid


def find_christmas_tree(input_file: str, max_seconds: int = 10_000):
    robots = read_in_robots(input_file)
    for seconds in range(max_seconds):
        current_grid = plot_grid_for_one_time(robots, seconds)
        grid_as_string = ["".join(line) for line in current_grid]
        with open("day14/find_a_tree.txt", "a") as tree_file:
            tree_file.write("--------------------\n")
            tree_file.write(f"{seconds=}")
            for line in grid_as_string:
                tree_file.write(f"{line}\n")
            tree_file.write("--------------------\n")


def print_found_tree(input_file: str):
    robots = read_in_robots(input_file)
    current_grid = plot_grid_for_one_time(robots, 6475)
    grid_as_string = ["".join(line) for line in current_grid]
    for line in grid_as_string:
        print(line)


if __name__ == "__main__":
    print(calculate_safety_factor_p1("day14/day14_final_input.txt"))
    find_christmas_tree("day14/day14_final_input.txt")
    # found tree at 6475!
    print_found_tree("day14/day14_final_input.txt")

import numpy as np
import copy


def read_in_farm(input_file) -> np.ndarray:
    with open(input_file) as raw_farm:
        return np.array([[*line.strip()] for line in raw_farm.readlines()])


def get_orthogonal_plants(point: tuple[int]):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    return [
        (point[0] + direction[0], point[1] + direction[1]) for direction in directions
    ]


def point_is_in_grid(pos: tuple[int], grid: np.ndarray) -> bool:
    row, column = pos
    max_row, max_column = grid.shape
    if row < 0 or column < 0 or row > max_row - 1 or column > max_column - 1:
        return False
    return True


def count_perimeter_walls(plant_type: str, point: tuple[int], farm: np.ndarray) -> int:
    count = 0
    for point in get_orthogonal_plants(point):
        if not point_is_in_grid(point, farm):
            count += 1
        elif farm[point] != plant_type:
            count += 1
    return count


def get_all_surrounding_points(point: tuple[int]) -> list[tuple[int]]:
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, -1), (1, 1), (-1, 1)]
    return [
        (point[0] + direction[0], point[1] + direction[1]) for direction in directions
    ]


def get_perimeter_walls(plant_type: str, point: tuple[int], farm: np.ndarray) -> int:
    perimeter_walls = []
    for point in get_all_surrounding_points(point):
        if not point_is_in_grid(point, farm):
            perimeter_walls.append(point)
        elif farm[point] != plant_type:
            perimeter_walls.append(point)
    return set(perimeter_walls)


def find_regions_better(farm: np.ndarray) -> dict[int : set[tuple[int]]]:
    all_regions = {}
    region_number = 0
    seen_plants = set()
    for row_id, row in enumerate(farm):
        for col_id, plant in enumerate(row):
            if (coord := (row_id, col_id)) not in seen_plants:
                seen_plants.add(coord)
                growing_region = {coord}
                final_region = set()
                while growing_region:
                    current_coord = growing_region.pop()
                    final_region.add(current_coord)
                    for orthogonal_plant in get_orthogonal_plants(current_coord):
                        if (
                            point_is_in_grid(orthogonal_plant, farm)
                            and farm[orthogonal_plant] == plant
                            and orthogonal_plant not in seen_plants
                        ):
                            growing_region.add(orthogonal_plant)
                            seen_plants.add(orthogonal_plant)
                region_number += 1
                all_regions[region_number] = final_region
    return all_regions


def plot_int_grid(farm: np.ndarray, all_regions: dict[int : set[int]]) -> np.ndarray:
    new_grid = np.zeros(farm.shape)
    for plant_type, region in all_regions.items():
        for point in region:
            new_grid[point] = plant_type
    return new_grid


def calculate_answer_p1(input_file: str) -> int:
    farm = read_in_farm(input_file)
    integer_regions = find_regions_better(farm)
    farm_as_ints = plot_int_grid(farm, integer_regions)
    price = 0
    for plant_id, region in integer_regions.items():
        area = len(region)
        perimeter = 0
        for point in region:
            perimeter += count_perimeter_walls(plant_id, point, farm_as_ints)
        price += area * perimeter
    return price


def plot_big_grid(farm: np.ndarray, all_regions: dict[int : set[int]]) -> np.ndarray:
    new_grid = np.zeros(farm.shape)
    for plant_type, region in all_regions.items():
        for point in region:
            new_grid[point] = plant_type
    big_grid = np.kron(new_grid, np.ones((4, 4)))
    return np.pad(big_grid, (1, 1), constant_values=0)


def get_topmost_leftmost_point(points: set[tuple[int]]) -> tuple[int]:
    rows = [point[0] for point in points]
    top_row = min(rows)
    points_on_row = [point[1] for point in points if point[0] == top_row]
    return (top_row, min(points_on_row))


def get_ordered_points(points: set[tuple[int]]) -> list[int]:
    all_border_boys = []
    region_to_edit = copy.deepcopy(points)
    rows = [point[0] for point in region_to_edit]
    top_row = min(rows)
    points_on_row = [point[1] for point in region_to_edit if point[0] == top_row]
    current_point = (top_row, min(points_on_row))
    current_ordered_region = [current_point]
    region_to_edit.remove(current_point)
    while region_to_edit:
        found_point = False
        for point in get_orthogonal_plants(current_point):
            if point in region_to_edit:
                current_ordered_region.append(point)
                region_to_edit.remove(point)
                current_point = point
                found_point = True
                break
        if not found_point and region_to_edit:
            all_border_boys.append(current_ordered_region)
            rows = [point[0] for point in region_to_edit]
            top_row = min(rows)
            points_on_row = [
                point[1] for point in region_to_edit if point[0] == top_row
            ]
            current_point = (top_row, min(points_on_row))
            current_ordered_region = [current_point]
            region_to_edit.remove(current_point)
    all_border_boys.append(current_ordered_region)
    return all_border_boys


# create traverse points by editing above
# get top left point
# if there is a point in points that is orthogonal
# get this point, and find the direction
# remove point from points
# set this to current direction
# add one to the side count
# if there isnt a point that is orthogonal, find new top left point
# remove point from points
# add one to side count
# continue


def get_sides_for_this_boy(ordered_points):
    current_direction = (0, 0)
    side_count = 0
    for point_1, point_2 in zip(ordered_points, ordered_points[1:]):
        direction = (point_2[0] - point_1[0], point_2[1] - point_1[1])
        if direction != current_direction:
            current_direction = direction
            side_count += 1
    return side_count


def get_number_of_sides(region_number: set[tuple[int]], big_grid: np.ndarray) -> int:
    region_rows, region_columns = np.where(big_grid == region_number)
    all_perimeter_walls = set()
    for row, column in zip(region_rows, region_columns):
        all_perimeter_walls = all_perimeter_walls.union(
            get_perimeter_walls(region_number, (row, column), big_grid)
        )
    ordered_points = get_ordered_points(all_perimeter_walls)
    side_count = 0
    for points in ordered_points:
        side_count += get_sides_for_this_boy(points)
    return side_count


def calculate_answer_p2(input_file: str) -> int:
    farm = read_in_farm(input_file)
    integer_regions = find_regions_better(farm)
    big_grid = plot_big_grid(farm, integer_regions)
    price = 0
    for plant_id, region in integer_regions.items():
        area = len(region)
        no_sides = get_number_of_sides(plant_id, big_grid)
        price += area * no_sides
    return price


if __name__ == "__main__":
    print(calculate_answer_p1("day12/day12_final_input.txt"))
    print(calculate_answer_p2("day12/day12_final_input.txt"))

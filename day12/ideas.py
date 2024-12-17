def count_perimeter_sides(surrounding_points: list[int]) -> int:
    side_count = 1
    surrounding_points_distinct = set(surrounding_points)
    rows = [point[0] for point in surrounding_points]
    top_row = min(rows)
    points_on_row = [point[1] for point in surrounding_points if point[0] == top_row]
    current_point = (top_row, min(points_on_row))
    surrounding_points_distinct.remove(current_point)
    current_direction = (0,1)
    # print(current_point)
    while surrounding_points_distinct:
        new_point_found = False
        potential_point_1 = (current_direction[0] + current_point[0], current_direction[1] + current_point[1])
        if potential_point_1 in surrounding_points_distinct:
            # print(f'new point is {potential_point_1}')
            new_point = potential_point_1
            surrounding_points_distinct.remove(new_point)
            current_point = new_point
            new_point_found = True
        else:
            # print(f'jumping off point = {potential_point_1}')
            new_point, new_direction = find_new_point_and_direction(potential_point_1, current_direction, surrounding_points_distinct)
            surrounding_points_distinct.remove(new_point)
            new_point_found = True
            side_count += 1
            current_direction = new_direction
            # print(f'new side! side number is {side_count}')
            # print(f'new point is {new_point}')
            # print(f'new direction is {current_direction}')
        current_point = new_point
        # print(f'current point = {current_point}')
        if not new_point_found:
            # print('oops')
            break
        # print(f'remaining points = {surrounding_points_distinct}')
    return side_count

def find_new_point_and_direction(potential_point_1: tuple[int], current_direction: tuple[int], surrounding_points_distinct: set[tuple[int]]) -> tuple[int]:
    # print('---------')
    # print('in find new point function')
    # print(surrounding_points_distinct)
    if current_direction == (0,1) or current_direction == (0,-1):
        potential_point_2 = (potential_point_1[0]-1, potential_point_1[1])
        potential_point_3 = (potential_point_1[0]+1, potential_point_1[1])
        # print(f'{potential_point_2=}')
        # print(f'{potential_point_3=}')
        if potential_point_2 in surrounding_points_distinct:
            return potential_point_2, (-1, 0)
        if potential_point_3 in surrounding_points_distinct:
            return potential_point_3, (1, 0)
    if current_direction == (1,0) or current_direction == (-1,0):
        potential_point_4 = (potential_point_1[0], potential_point_1[1]-1)
        potential_point_5 = (potential_point_1[0], potential_point_1[1]+1)
        # print(f'{potential_point_4=}')
        # print(f'{potential_point_5=}')
        if potential_point_4 in surrounding_points_distinct:
            return potential_point_4, (0,-1)
        if potential_point_5 in surrounding_points_distinct:
            return potential_point_5, (0, 1)
        
# def get_all_surrounding_points(point: tuple[int]):
#     directions = [(1,0), (-1,0), (0,1), (0,-1), (-1, -1), (1, -1), (1,1), (-1,1)]
#     return [(point[0]+direction[0], point[1]+direction[1]) for direction in directions]

def get_perimeter_points(plant_type: str, point: tuple[int], farm: np.ndarray) -> list[int]:
    surrounding_points = []
    for point in get_orthogonal_points(point):
        if not pos_is_in_grid(point, farm):
            surrounding_points.append(point)
        elif farm[point] != plant_type:
            surrounding_points.append(point)
    return surrounding_points 

def plot_regions_on_double_size_grid(region: set[tuple[int]], plant_type: str) -> np.ndarray:
    coords_doubled = [(coord[0] * 2 + 2, coord[1] * 2 + 2) for coord in region]
    max_row = max([coord[0] for coord in coords_doubled]) + 2
    max_column = max([coord[1] for coord in coords_doubled]) + 2
    new_grid = np.full((max_row, max_column), '.')
    for coord in coords_doubled:
        new_grid[coord] = plant_type
    return new_grid
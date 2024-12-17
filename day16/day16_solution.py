import numpy as np
import heapq

def read_in_maze(input_file) -> np.ndarray:
    with open(input_file) as raw_maze:
        return np.array([[*line.strip()] for line in raw_maze.readlines()])
    
DIR_MAP = {(1,0): [(0,1), (0,-1)], (-1,0): [(0,1), (0,-1)], (0,1): [(1,0), (-1,0)], (0,-1): [(1,0), (-1,0)]}

def find_shortest_path(input_file: str) -> int:
    maze = read_in_maze(input_file)
    start_point = (np.where(maze=='S')[0][0], np.where(maze=='S')[1][0])
    seen_paths = {(start_point, (0,1))}
    all_paths = [(0, start_point, (0,1))]
    heapq.heapify(all_paths)
    while all_paths:
        score, position, direction = heapq.heappop(all_paths)
        #create function so not doubling effort
        new_pos_straight = (position[0]+direction[0], position[1]+direction[1])
        if maze[new_pos_straight] == 'E':
            return score + 1
        if maze[new_pos_straight] != '#' and (new_pos_straight, direction) not in seen_paths:
            heapq.heappush(all_paths, (score+1, new_pos_straight, direction))
            seen_paths.add((new_pos_straight, direction))
        for perp_direction in DIR_MAP[direction]:
            new_pos_perp = (position[0]+perp_direction[0], position[1]+perp_direction[1])
            if maze[new_pos_perp] == 'E':
                return score + 1001
            if maze[new_pos_perp] != '#' and (new_pos_perp, perp_direction) not in seen_paths:
                heapq.heappush(all_paths, (score+1001, new_pos_perp, perp_direction))
                seen_paths.add((new_pos_perp, perp_direction))

def find_shortest_scores(maze: np.ndarray, max_score: int) -> int:
    print(f'score to get {max_score}')
    start_point = (np.where(maze=='S')[0][0], np.where(maze=='S')[1][0])
    shortest_scores = {}
    seen_paths = {(0, start_point, (0,1), False)}
    all_paths = [(0, start_point, (0,1), False)]
    heapq.heapify(all_paths)
    loops = 0
    while all_paths:
        loops += 1
        if loops % 100000 == 0:
            print(f'first loop: {score}')
        score, position, current_direction, turned = heapq.heappop(all_paths)
        
        
        if score > max_score:
            return shortest_scores
        shortest_scores.setdefault(position, []).append((score, current_direction, turned))
        #create function so not doubling effort
        new_pos_straight = (position[0]+current_direction[0], position[1]+current_direction[1])
        if maze[new_pos_straight] == 'E':
            seen_paths.add((score+1, new_pos_straight, current_direction, False))
            shortest_scores.setdefault(new_pos_straight, []).append((score+1, current_direction, False))
            continue
        if maze[new_pos_straight] != '#' and (score+1, new_pos_straight, current_direction, False) not in seen_paths:
            heapq.heappush(all_paths, (score+1, new_pos_straight, current_direction, False))
            seen_paths.add((score+1, new_pos_straight, current_direction, False))
        for perp_direction in DIR_MAP[current_direction]:
            new_pos_perp = (position[0]+perp_direction[0], position[1]+perp_direction[1])
            if maze[new_pos_perp] == 'E':
                seen_paths.add((score+1001, new_pos_perp, perp_direction, True))
                shortest_scores.setdefault(new_pos_perp, []).append((score+1001, perp_direction, True))
                continue
            if maze[new_pos_perp] != '#' and (score+1001, new_pos_perp, perp_direction, True) not in seen_paths:
                heapq.heappush(all_paths, (score+1001, new_pos_perp, perp_direction, True))
                seen_paths.add((score+1001, new_pos_perp, perp_direction, True))
    

def plot_scores(maze_shape: tuple[int], scores: list[tuple[int, tuple[int]]], max_score: int) -> np.ndarray:
    new_maze = np.full(maze_shape, max_score + 1)
    for score, position in scores:
        new_maze[position] = score
    return new_maze

def find_all_points_on_shortest_path(input_file: str) -> int:
    maze = read_in_maze(input_file)
    max_score = find_shortest_path(input_file)
    point_to_scores = find_shortest_scores(maze, max_score)
    end_point = (np.where(maze=='E')[0][0], np.where(maze=='E')[1][0])
    seen_paths = set()
    final_points = set()
    all_paths = [(score, end_point, direction, turned) for score, direction, turned in point_to_scores[end_point]]
    heapq.heapify(all_paths)
    while all_paths:
        score, position, direction, turned = heapq.heappop(all_paths)
        new_pos = (position[0]-direction[0], position[1]-direction[1])
        print(score)
        if (score, position, direction, turned) not in seen_paths and new_pos in point_to_scores:
            score_to_find = score - 1001 if turned else score - 1
            for path in point_to_scores[new_pos]:
                if path[0] == score_to_find:
                    new_path = (path[0], new_pos, path[1], path[2])
                    heapq.heappush(all_paths, new_path)
        seen_paths.add((score, position, direction, turned))
        final_points.add(position)
    return len(final_points)

    
if __name__ == "__main__":
    print(find_shortest_path("day16/day16_final_input.txt"))
    #this takes 7 minutes, try optimise
    print(find_all_points_on_shortest_path("day16/day16_final_input.txt"))

    

import numpy as np
import heapq


def read_in_falling_bytes(input_file: str) -> list[int]:
    with open(input_file) as raw_bytes:
        return [
            tuple(map(int, line.strip().split(","))) for line in raw_bytes.readlines()
        ]


directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def is_pos_in_grid(pos: tuple[int], max_xy: int) -> bool:
    for coord in pos:
        if coord < 0 or coord > max_xy:
            return False
    return True


def find_path(fallen_bytes: list[int], max_xy: int = 70) -> int:
    all_paths = [(0, (0, 0))]
    seen_paths = set()
    heapq.heapify(all_paths)
    while all_paths:
        current_steps, current_position = heapq.heappop(all_paths)
        if current_position not in seen_paths:
            for next_direction in directions:
                next_position = (
                    current_position[0] + next_direction[0],
                    current_position[1] + next_direction[1],
                )
                if next_position == (max_xy, max_xy):
                    return current_steps + 1
                if next_position not in fallen_bytes and is_pos_in_grid(
                    next_position, max_xy
                ):
                    heapq.heappush(all_paths, (current_steps + 1, next_position))
            seen_paths.add(current_position)


def find_blocking_point(input_file: str, max_xy: int = 70, no_fallen_bytes: int = 1024):
    all_bytes = read_in_falling_bytes(input_file)
    while find_path(all_bytes[:no_fallen_bytes], max_xy) is not None:
        no_fallen_bytes += 1
    return all_bytes[no_fallen_bytes - 1]


if __name__ == "__main__":
    print(find_path(read_in_falling_bytes("day18/day18_final_input.txt")[:1024]))
    # try a cleverer method to get part 2 that doesnt take 3 minutes!
    print(find_blocking_point("day18/day18_final_input.txt"))

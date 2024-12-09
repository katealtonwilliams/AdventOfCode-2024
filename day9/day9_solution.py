import numpy as np


def read_in_disk_map(input_file) -> list[tuple[int]]:
    with open(input_file) as raw_map:
        full_map = raw_map.read() + "0"
    return np.array(
        [(int(full_map[i]), int(full_map[i + 1])) for i in range(0, len(full_map), 2)]
    )


def build_blocks(full_map: np.ndarray[tuple[int]]) -> np.ndarray[ImportWarning]:
    row_id = 0
    all_blocks = np.array([])
    all_numbers = np.array([])
    for pair in full_map:
        all_numbers = np.concatenate((all_numbers, np.full((pair[0],), row_id)))
        all_blocks = np.concatenate(
            (all_blocks, np.full((pair[0],), row_id), np.full((pair[1],), -1))
        )
        row_id += 1
    return np.array(all_blocks), np.array(all_numbers[::-1])


def calculate_checksum(all_blocks: np.ndarray) -> int:
    check_sum = 0
    for index, number in enumerate(all_blocks):
        if number != -1:
            check_sum += index * int(number)
    return check_sum


def calculate_checksum_p1(input_file: str) -> int:
    disk_map = read_in_disk_map(input_file)
    all_blocks, block_index = build_blocks(disk_map)
    for replace_block in block_index:
        if len(replace_positions := np.where(all_blocks == -1)[0]) != 0:
            all_blocks[replace_positions[0]] = replace_block
            all_blocks = all_blocks[:-1]
        else:
            all_blocks = all_blocks[: len(block_index)]
            break
    return calculate_checksum(all_blocks)


def find_destination_indices(block_length: int, can_move_to: np.ndarray) -> np.ndarray:
    empty_positions = np.where(can_move_to == -1)[0]
    possible_dest_blocks = np.split(
        empty_positions, np.where(np.diff(empty_positions) != 1)[0] + 1
    )
    possible_dest_blocks_lengths = np.array(
        [len(positions) for positions in possible_dest_blocks]
    )
    if (
        len(
            possible_dest_indices := np.where(
                possible_dest_blocks_lengths >= block_length
            )[0]
        )
        != 0
    ):
        return possible_dest_blocks[possible_dest_indices[0]]
    return None


def calculate_checksum_p2(input_file: str) -> int:
    disk_map = read_in_disk_map(input_file)
    all_blocks, blocks_to_move = build_blocks(disk_map)
    block_id = max(blocks_to_move) + 1
    for replace_block in disk_map[::-1]:
        block_id -= 1
        block_length = replace_block[0]
        block_start_positions = np.where(all_blocks == block_id)[0]
        can_move_to = all_blocks[: block_start_positions[0]]
        if -1 in can_move_to:
            if (
                dest_indices := find_destination_indices(block_length, can_move_to)
            ) is not None:
                for replace_index in range(block_length):
                    all_blocks[dest_indices[replace_index]] = block_id
                for remove_index in block_start_positions:
                    all_blocks[remove_index] = -1
            else:
                continue
        else:
            break
    return calculate_checksum(all_blocks)


if __name__ == "__main__":
    print(calculate_checksum_p1("day9/day9_final_input.txt"))
    print(calculate_checksum_p2("day9/day9_final_input.txt"))

import copy


def read_in_stones(input_file) -> list[int]:
    with open(input_file) as raw_stones:
        return list(map(int, raw_stones.read().strip().split()))


def blink_once(number: int) -> list[int]:
    if number == 0:
        return [1]
    if (length := len(number_to_split := str(int(number)))) % 2 == 0:
        return [
            int(number_to_split[: int(length / 2)]),
            int(number_to_split[int(length / 2) :]),
        ]
    return [2024 * number]


def run_simulation(input_file: str, no_blinks: int = 25) -> int:
    current_stones = {stone: 1 for stone in map(int, read_in_stones(input_file))}
    current_blinks = 0
    while current_blinks < no_blinks:
        current_keys_values = copy.deepcopy(list(current_stones.items()))
        for current_stone, current_value in current_keys_values:
            current_stones[current_stone] -= current_value
            if current_stones[current_stone] == 0:
                del current_stones[current_stone]
            for proccessed_stone in blink_once(current_stone):
                current_stones[proccessed_stone] = (
                    current_stones.setdefault(proccessed_stone, 0) + current_value
                )
        current_blinks += 1
    return sum(current_stones.values())


if __name__ == "__main__":
    print(run_simulation("day11/day11_final_input.txt"))
    print(run_simulation("day11/day11_final_input.txt", 75))

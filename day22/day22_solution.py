def read_secret_numbers(input_file: str) -> list[int]:
    with open(input_file) as raw_numbers:
        return [int(line.strip()) for line in raw_numbers.readlines()]


def mix(secret_number: int, other_value: int) -> int:
    return secret_number ^ other_value


def prune(secret_number: int) -> int:
    return secret_number % 16777216


def mutiply(secret_number: int, factor: int) -> int:
    current_number = mix(secret_number, secret_number * factor)
    return prune(current_number)


def divide(secret_number: int, divider: int) -> int:
    current_number = mix(secret_number, secret_number // divider)
    return prune(current_number)


def find_next_secret_number(secret_number: int) -> int:
    current_number = mutiply(secret_number, 64)
    current_number = divide(current_number, 32)
    return mutiply(current_number, 2048)


def get_next_secret_number(first_number: int):
    current_number = first_number
    for _ in range(2000):
        current_number = find_next_secret_number(current_number)
    return current_number


def sum_secret_numbers(input_file: str) -> int:
    first_numbers = read_secret_numbers(input_file)
    secret_number_sum = 0
    for number in first_numbers:
        secret_number_sum += get_next_secret_number(number)
    return secret_number_sum


def get_differences_windows(first_number: int) -> dict[tuple:int]:
    current_number = first_number
    last_digit = int(str(first_number)[-1])
    current_window = ()
    changes_map = {}
    seen_changes = set()
    for i in range(2000):
        new_number = find_next_secret_number(current_number)
        new_last_digit = int(str(new_number)[-1])
        if i >= 4:
            current_window = current_window[1:] + (new_last_digit - last_digit,)
            if current_window not in seen_changes:
                changes_map[current_window] = new_last_digit
                seen_changes.add(current_window)
        else:
            current_window = current_window + (new_last_digit - last_digit,)
        current_number = new_number
        last_digit = new_last_digit
    return changes_map


def find_highest_number_of_bananas(input_file: str) -> int:
    all_changes_maps = []
    first_numbers = read_secret_numbers(input_file)
    for number in first_numbers:
        all_changes_maps.append(get_differences_windows(number))
    seen_change_comb = set()
    max_bananas = 0
    for _, change_map in enumerate(all_changes_maps):
        for change_comb in change_map.keys():
            if change_comb not in seen_change_comb:
                total_bananas = sum(
                    [change_map.get(change_comb, 0) for change_map in all_changes_maps]
                )
                seen_change_comb.add(change_comb)
                if total_bananas > max_bananas:
                    max_bananas = total_bananas
    return max_bananas


if __name__ == "__main__":
    print(sum_secret_numbers("day22/day22_final_input.txt"))
    print(find_highest_number_of_bananas("day22/day22_final_input.txt"))

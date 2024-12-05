import functools


def read_in_rules(input_file: str) -> tuple[set[str], list[tuple[str]], list[str]]:
    all_numbers = set()
    orders = []
    updates = []
    with open(input_file) as raw_rules_and_updates:
        all_lines = raw_rules_and_updates.readlines()
    for line_number, line in enumerate(all_lines):
        if line.strip() == "":
            break
        order = tuple(line.strip().split("|"))
        orders.append(order)
        for number in order:
            all_numbers.add(number)
    for line in all_lines[line_number + 1 :]:
        updates.append(line.strip())
    return all_numbers, orders, updates


def create_order_map(
    all_numbers: set[str], orders: list[tuple[str]]
) -> dict[dict[list[str]]]:
    order_map = {}
    for number in all_numbers:
        number_map = {"before": [], "after": []}
        for pair in orders:
            if number == pair[0]:
                number_map["after"].append(pair[1])
            if number == pair[1]:
                number_map["before"].append(pair[0])
        order_map[number] = number_map
    return order_map


def find_correct_updates(input_file: str) -> int:
    all_numbers, orders, updates = read_in_rules(input_file)
    order_map = create_order_map(all_numbers, orders)
    correct_middles = []
    for update in updates:
        found_incorrect_order = False
        for number in all_numbers:
            number_map = order_map[number]
            if number in update:
                split_update = update.split(number)
            else:
                continue
            if any(before in split_update[1] for before in number_map["before"]):
                found_incorrect_order = True
                break
            if any(after in split_update[0] for after in number_map["after"]):
                found_incorrect_order = True
                break
        if found_incorrect_order == False:
            update = update.split(",")
            middle = update[len(update) // 2]
            correct_middles.append(int(middle))
    return sum(correct_middles)


def get_compare_func(order_map: dict[dict[list[str]]]):
    def compare_numbers(left: str, right: str) -> int:
        left_map = order_map.get(left, {})
        right_map = order_map.get(right, {})
        if left_map == {} and right_map == {}:
            return 0
        if (
            left not in right_map.get("before", [])
            and left not in right_map.get("after", [])
            and right not in left_map.get("before", [])
            and right not in left_map.get("after", [])
        ):
            return 0
        if left in right_map.get("after", []):
            return 1
        if right in left_map.get("before", []):
            return 1
        return -1

    return compare_numbers


def find_incorrect_updates(input_file: str) -> int:
    all_numbers, orders, updates = read_in_rules(input_file)
    order_map = create_order_map(all_numbers, orders)
    compare_func = get_compare_func(order_map)
    corrected_middles = []
    for update in updates:
        update = update.split(",")
        update_sorted = sorted(update, key=functools.cmp_to_key(compare_func))
        if update != update_sorted:
            middle = update_sorted[len(update) // 2]
            corrected_middles.append(int(middle))
    return sum(corrected_middles)


if __name__ == "__main__":
    print(find_correct_updates("day5/day5_final_input.txt"))
    print(find_incorrect_updates("day5/day5_final_input.txt"))

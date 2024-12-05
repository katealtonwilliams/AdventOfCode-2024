import functools
from typing import Callable


def read_in_rules(input_file: str) -> tuple[dict[str:set], list[str]]:
    with open(input_file) as raw_orders_and_updates:
        orders_and_updates = [
            line.strip() for line in raw_orders_and_updates.readlines()
        ]
    blank_line = orders_and_updates.index("")
    orders = [tuple(order.split("|")) for order in orders_and_updates[:blank_line]]
    updates = [update.split(",") for update in orders_and_updates[blank_line + 1 :]]
    return create_order_map(orders), updates


def create_order_map(orders: list[tuple[str]]) -> dict[str:set]:
    order_map = {}
    for order in orders:
        order_map.setdefault(order[0], set()).add(order[1])
    return order_map


def found_incorrect_order(update: list[str], orders: dict[str:set]) -> bool:
    for index, number in enumerate(update):
        correct_after = orders.get(number, set())
        if any(after in update[:index] for after in correct_after):
            return True
    return False


def find_correct_updates(input_file: str) -> int:
    orders, updates = read_in_rules(input_file)
    return sum(
        int(update[len(update) // 2])
        for update in updates
        if not found_incorrect_order(update, orders)
    )


def get_compare_func(orders: dict[str:set]) -> Callable:
    def compare_numbers(left: str, right: str) -> int:
        if right in orders.get(left, []):
            return 1
        if left in orders.get(right, []):
            return -1
        return 0

    return compare_numbers


def find_incorrect_updates(input_file: str) -> int:
    orders, updates = read_in_rules(input_file)
    cmp = functools.cmp_to_key(get_compare_func(orders))
    return sum(
        int(sorted(update, key=cmp)[len(update) // 2])
        for update in updates
        if found_incorrect_order(update, orders)
    )


if __name__ == "__main__":
    print(find_correct_updates("day5/day5_final_input.txt"))
    print(find_incorrect_updates("day5/day5_final_input.txt"))

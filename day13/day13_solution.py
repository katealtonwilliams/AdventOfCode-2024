import re
from typing import Callable


def read_in_machines(input_file: str) -> list[dict]:
    with open(input_file) as raw_machines:
        all_machines = raw_machines.read()
    all_machines = all_machines.split("\n")
    all_machines = [
        (all_machines[i], all_machines[i + 1], all_machines[i + 2])
        for i in range(0, len(all_machines) - 4, 4)
    ]
    button_regex = r"Button [A|B]: X\+(\d+), Y\+(\d+)"
    prize_regex = r"Prize: X=(\d+), Y=(\d+)"
    clean_machines = []
    for machine in all_machines:
        a, b, target = machine
        clean_machine = {}
        clean_machine["A"] = re.findall(button_regex, a)[0]
        clean_machine["B"] = re.findall(button_regex, b)[0]
        clean_machine["target"] = re.findall(prize_regex, target)[0]
        clean_machines.append(clean_machine)
    return clean_machines


def solve_equations_p1(machine: dict[str:list]) -> int | None:
    x1, y1 = map(int, machine["A"])
    x2, y2 = map(int, machine["B"])
    target_x, target_y = map(int, machine["target"])
    b = (x1 * target_y - y1 * target_x) / (x1 * y2 - x2 * y1)
    if b > 100 or not b.is_integer():
        return None
    a = (target_x - b * x2) / x1
    if a > 100 or not a.is_integer():
        return None
    return a * 3 + b


def solve_equations_p2(machine: dict[str:list]) -> int | None:
    x1, y1 = map(int, machine["A"])
    x2, y2 = map(int, machine["B"])
    target_x, target_y = map(int, machine["target"])
    target_x += 10000000000000
    target_y += 10000000000000
    b = (x1 * target_y - y1 * target_x) / (x1 * y2 - x2 * y1)
    if not b.is_integer():
        return None
    a = (target_x - b * x2) / x1
    if not a.is_integer():
        return None
    return a * 3 + b


def calculate_answer_p1(input_file: str, equation_solver: Callable) -> int:
    machines = read_in_machines(input_file)
    tokens = 0
    for machine in machines:
        if (solution := equation_solver(machine)) is not None:
            tokens += solution
    return tokens


if __name__ == "__main__":
    print(calculate_answer_p1("day13/day13_final_input.txt", solve_equations_p1))
    print(calculate_answer_p1("day13/day13_final_input.txt", solve_equations_p2))

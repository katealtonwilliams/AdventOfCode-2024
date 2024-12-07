import heapq

def read_in_equations(input_file: str) -> dict[int : list[int]]:
    with open(input_file) as raw_equations:
        all_equations = []
        for line in raw_equations.readlines():
            line = line.strip().split(":")
            all_equations.append((int(line[0]), list(map(int, line[1].split()))))
    return all_equations


def find_correct_equations_p1(input_file: str) -> int:
    all_equations = read_in_equations(input_file)
    total_calibration_result = 0
    for answer, numbers in all_equations:
        numbers_to_check = numbers[::-1]
        possible_equations = [(answer, 0)]
        heapq.heapify(possible_equations)
        while possible_equations:
            current_equation, next_index = heapq.heappop(possible_equations)
            if next_index == len(numbers_to_check) - 1:
                if current_equation == numbers_to_check[next_index]:
                    total_calibration_result += answer
                    break
            if next_index < len(numbers_to_check):
                check = numbers_to_check[next_index]
                if (remaining := current_equation - check) >= 0:
                    heapq.heappush(possible_equations, (remaining, next_index + 1))
                if (remaining := current_equation / check).is_integer():
                    heapq.heappush(possible_equations, (remaining, next_index + 1))
    return total_calibration_result


def find_correct_equations_p2(input_file: str) -> int:
    all_equations = read_in_equations(input_file)
    total_calibration_result = 0
    for answer, numbers_to_check in all_equations:
        possible_equations = [(answer, 0)]
        heapq.heapify(possible_equations)
        while possible_equations:
            remaining, next_index = heapq.heappop(possible_equations)
            if next_index == len(numbers_to_check):
                if remaining == 0:
                    total_calibration_result += answer
                    break
            current_equation = answer - remaining
            if next_index < len(numbers_to_check):
                check = numbers_to_check[next_index]
                if (next_equation := current_equation + check) <= answer:
                    heapq.heappush(
                        possible_equations, (answer - next_equation, next_index + 1)
                    )
                if (next_equation := current_equation * check) <= answer:
                    heapq.heappush(
                        possible_equations, (answer - next_equation, next_index + 1)
                    )
                if (next_equation := int(str(current_equation) + str(check))) <= answer:
                    heapq.heappush(
                        possible_equations, (answer - next_equation, next_index + 1)
                    )

    return total_calibration_result


if __name__ == "__main__":
    print(find_correct_equations_p1("day7/day7_final_input.txt"))
    print(find_correct_equations_p2("day7/day7_final_input.txt"))

import re

find_digit_regex = r"mul\((\d{1,3}),(\d{1,3})\)"


def find_answer_p1(input_file: str) -> int:
    total = 0
    with open(input_file) as raw_instructions:
        for line in raw_instructions.readlines():
            total += sum(
                int(ex[0]) * int(ex[1]) for ex in re.findall(find_digit_regex, line)
            )
    return total


def find_answer_p2(input_file: str) -> int:
    total = 0
    with open(input_file) as raw_instructions:
        full_line = ""
        for line in raw_instructions.readlines():
            full_line += line.strip()
    found_last_dont = False
    next_dont_index = full_line.find("don't()")
    next_do_index = 0
    while found_last_dont == False:
        if next_dont_index == -1:
            total += sum(
                int(ex[0]) * int(ex[1])
                for ex in re.findall(find_digit_regex, full_line[next_do_index:])
            )
            found_last_dont = True
            break
        total += sum(
            int(ex[0]) * int(ex[1])
            for ex in re.findall(
                find_digit_regex, full_line[next_do_index:next_dont_index]
            )
        )
        next_do_index = full_line.find("do()", next_dont_index + 1)
        next_dont_index = full_line.find("don't()", next_do_index + 1)
    return total


if __name__ == "__main__":
    print(find_answer_p1("day3/day3_final_input.txt"))
    print(find_answer_p2("day3/day3_final_input.txt"))

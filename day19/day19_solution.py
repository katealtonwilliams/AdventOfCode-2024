def read_in_designs(input_file: str) -> tuple[list[str], list[str]]:
    with open(input_file) as raw_designs:
        towels_and_designs = raw_designs.read()
    towels_and_designs = towels_and_designs.split("\n")
    blank_line_index = towels_and_designs.index("")
    towels = []
    for towel in towels_and_designs[:blank_line_index]:
        towels.extend(towel.split(", "))
    towels.sort(key=len, reverse=True)
    return towels, towels_and_designs[blank_line_index + 1 :]


def is_valid_design(design: str, towels: list[str]) -> bool:
    possible_towels = [towel for towel in towels if towel in design]
    possible_combinations = [""]
    seen_combinations = set()
    while possible_combinations:
        current_combination = possible_combinations.pop()
        if len(current_combination) == len(design):
            return True
        if current_combination not in seen_combinations:
            new_combinations = [
                current_combination + towel
                for towel in possible_towels
                if design.startswith(current_combination + towel)
            ]
            possible_combinations.extend(new_combinations)
            seen_combinations.add(current_combination)
    return False


def count_valid_combs_for_design(design: str, towels: list[str]) -> bool:
    possible_towels = [towel for towel in towels if towel in design]
    design_to_match = " " + design
    design_chunks = [design_to_match[:i] for i in range(2, len(design_to_match) + 1)]
    match_counter = {design_chunk: 0 for design_chunk in design_chunks}
    match_counter[" "] = 1
    for chunk in design_chunks:
        for towel in possible_towels:
            if chunk.endswith(towel):
                match_counter[chunk] += match_counter[chunk[: -len(towel)]]
    return match_counter[design_to_match]


def count_valid_designs(input_file: str) -> int:
    towels, designs = read_in_designs(input_file)
    valid_count = 0
    for design in designs:
        valid_count += is_valid_design(design, towels)
    return valid_count


def count_all_valid_towel_combs(input_file: str) -> int:
    towels, designs = read_in_designs(input_file)
    combinations_count = 0
    for design in designs:
        combinations_count += count_valid_combs_for_design(design, towels)
    return combinations_count


if __name__ == "__main__":
    print(count_valid_designs("day19/day19_final_input.txt"))
    print(count_all_valid_towel_combs("day19/day19_final_input.txt"))

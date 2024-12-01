def read_in_ids(input_file: str) -> tuple[list[str]]:
    with open(input_file) as raw_ids:
        left_ids = []
        right_ids = []
        for line in raw_ids.readlines():
            line = line.strip().split("  ")
            left_ids.append(int(line[0]))
            right_ids.append(int(line[1]))
    return left_ids, right_ids


def find_answer_p1(input_file: str) -> int:
    left_ids, right_ids = read_in_ids(input_file)
    left_ids.sort()
    right_ids.sort()
    differences = [abs(left - right) for left, right in zip(left_ids, right_ids)]
    return sum(differences)


def find_answer_p2(input_file: str) -> int:
    left_ids, right_ids = read_in_ids(input_file)
    similarity_scores = [left * (right_ids.count(left)) for left in left_ids]
    return sum(similarity_scores)


if __name__ == "__main__":
    print(find_answer_p1("day1/day1_final_input.txt"))
    print(find_answer_p2("day1/day1_final_input.txt"))

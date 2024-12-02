from itertools import combinations


def read_in_reports(input_file: str) -> list[list[int]]:
    with open(input_file) as raw_reports:
        all_reports = []
        for report in raw_reports.readlines():
            report = report.strip().split()
            all_reports.append(list(map(int, report)))
        return all_reports


def is_safe_report(report: list[int]) -> bool:
    neighbour_pairs = [(report[i], report[i + 1]) for i in range(len(report) - 1)]
    differences = [right - left for left, right in neighbour_pairs]
    if all(abs(difference) <= 3 for difference in differences):
        if all(difference < 0 for difference in differences):
            return True
        if all(difference > 0 for difference in differences):
            return True
    return False


def find_answer_p1(input_file: str) -> int:
    reports = read_in_reports(input_file)
    safe_report_count = 0
    for report in reports:
        if is_safe_report(report):
            safe_report_count += 1
    return safe_report_count


def find_answer_p2(input_file: str) -> int:
    reports = read_in_reports(input_file)
    safe_report_count = 0
    for report in reports:
        if is_safe_report(report):
            safe_report_count += 1
            continue
        for comb in combinations(report, len(report) - 1):
            if is_safe_report(comb):
                safe_report_count += 1
                break
    return safe_report_count


if __name__ == "__main__":
    print(find_answer_p1("day2/day2_final_input.txt"))
    print(find_answer_p2("day2/day2_final_input.txt"))

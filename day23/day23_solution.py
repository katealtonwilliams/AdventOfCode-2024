import numpy as np
from itertools import combinations


def read_in_connections(input_file: str) -> list[str]:
    with open(input_file) as raw_connections:
        return [(line.strip()) for line in raw_connections.readlines()]


def find_triples_with_ts(input_file: str) -> int:
    all_connections = read_in_connections(input_file)
    seen_triples = []
    starts_with_t_count = 0
    for connection in all_connections:
        con1, con2 = connection.split("-")
        con1_connections = {
            con.replace("-", "").replace(con1, "")
            for con in all_connections
            if con1 in con
        }
        con2_connections = {
            con.replace("-", "").replace(con2, "")
            for con in all_connections
            if con2 in con
        }
        mutual_connections = (con2_connections & con1_connections) - {con1, con2}
        triples = [{con1, con2, mut} for mut in mutual_connections]
        for triple in triples:
            if triple not in seen_triples:
                if any(con.startswith("t") for con in triple):
                    starts_with_t_count += 1
                    seen_triples.append(triple)
    return starts_with_t_count


def find_bin_connections_for_each_comp(
    all_connections: list[str],
) -> tuple[list[str], list[str]]:
    computer_names = set()
    for connection in all_connections:
        computers = connection.split("-")
        computer_names.add(computers[0])
        computer_names.add(computers[1])
    computer_names = list(computer_names)
    bin_cons_for_comps = []
    for idx, comp in enumerate(computer_names):
        connections = {
            con.replace("-", "").replace(comp, "")
            for con in all_connections
            if comp in con
        }
        connections_binary = [
            "1" if comp in connections else "0" for comp in computer_names
        ]
        connections_binary[idx] = "1"
        connections_binary = format("".join(connections_binary))
        bin_cons_for_comps.append(connections_binary)
    return bin_cons_for_comps, computer_names


def find_biggest_interconnected_group_for_comp(
    comp_to_test: int, bin_cons_for_comps: list[int], current_max: int
) -> tuple[int, int] | None:
    connected_comps = np.array(
        [
            int(bin_cons_for_comps[i], 2)
            for i in range(len(comp_to_test))
            if comp_to_test[i] == "1"
        ]
    )
    group_size = len(connected_comps)
    while group_size > current_max:
        connected_comp_combs = combinations(connected_comps, group_size)
        for comb in connected_comp_combs:
            bitwise_and_all_comps = np.bitwise_and.reduce(comb)
            if bitwise_and_all_comps.bit_count() == group_size:
                return bitwise_and_all_comps, group_size
        group_size -= 1
    return None


def find_overall_biggest_group(input_file: str) -> str:
    connections = read_in_connections(input_file)
    bin_cons_for_comps, computer_names = find_bin_connections_for_each_comp(connections)
    current_max = 3
    for connection in bin_cons_for_comps:
        if (
            found_group := find_biggest_interconnected_group_for_comp(
                connection, bin_cons_for_comps, current_max
            )
        ) is not None:
            biggest_group, current_max = found_group
    biggest_group = format(biggest_group, f"0{len(computer_names)}b")
    biggest_group = [
        computer_names[i] for i in range(len(computer_names)) if biggest_group[i] == "1"
    ]
    biggest_group.sort()
    return ",".join(biggest_group)


if __name__ == "__main__":
    print(find_triples_with_ts("day23/day23_final_input.txt"))
    print(find_overall_biggest_group("day23/day23_final_input.txt"))

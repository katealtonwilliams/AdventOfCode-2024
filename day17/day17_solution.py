import re
import heapq


def read_in_program(input_file: str) -> tuple[dict[str:int], list[int]]:
    with open(input_file) as raw_program:
        register_and_instructions = raw_program.read()
    register_and_instructions = register_and_instructions.split("\n")
    register_pattern = r" (A|B|C): (.*)"
    registers = {
        re.findall(register_pattern, line)[0][0]: int(
            re.findall(register_pattern, line)[0][1]
        )
        for line in register_and_instructions[:-2]
    }
    instructions = list(
        map(int, re.findall(r": (.*)", register_and_instructions[-1])[0].split(","))
    )
    return registers, instructions


def get_combo_operand(literal_operand: int, registers: dict[str:int]) -> int:
    if literal_operand in [0, 1, 2, 3]:
        return literal_operand
    if literal_operand == 4:
        return registers["A"]
    if literal_operand == 5:
        return registers["B"]
    if literal_operand == 6:
        return registers["C"]


def adv(
    literal_operand: int | str, registers: dict[str:int]
) -> tuple[str, int, None, None]:
    return (
        "A",
        int(registers["A"] / 2 ** get_combo_operand(literal_operand, registers)),
        None,
        None,
    )


def bxl(
    literal_operand: int | str, registers: dict[str:int]
) -> tuple[str, int, None, None]:
    return "B", literal_operand ^ registers["B"], None, None


def bst(
    literal_operand: int | str, registers: dict[str:int]
) -> tuple[str, int, None, None]:
    return "B", get_combo_operand(literal_operand, registers) % 8, None, None


def jnz(
    literal_operand: int | str, registers: dict[str:int]
) -> tuple[None, None, int | None, None]:
    if registers["A"] == 0:
        return None, None, None, None
    else:
        return None, None, literal_operand, None


def bxc(
    literal_operand: int | str, registers: dict[str:int]
) -> tuple[str, int, None, None]:
    return "B", registers["B"] ^ registers["C"], None, None


def out(
    literal_operand: int | str, registers: dict[str:int]
) -> tuple[None, None, None, int]:
    return None, None, None, get_combo_operand(literal_operand, registers) % 8


def bdv(
    literal_operand: int | str, registers: dict[str:int]
) -> tuple[str, int, None, None]:
    return (
        "B",
        int(registers["A"] / 2 ** get_combo_operand(literal_operand, registers)),
        None,
        None,
    )


def cdv(
    literal_operand: int | str, registers: dict[str:int]
) -> tuple[str, int, None, None]:
    return (
        "C",
        int(registers["A"] / 2 ** get_combo_operand(literal_operand, registers)),
        None,
        None,
    )


OPCODE_DICT = {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}


def do_step_until_next_out(
    pointer: int, instructions: list[int], registers: dict[str:int], current_out: str
) -> str:
    while pointer < len(instructions):
        opcode = instructions[pointer]
        instruction_func = OPCODE_DICT[opcode]
        literal_operand = instructions[pointer + 1]
        register_to_update, value_to_update, next_pointer, out_value = instruction_func(
            literal_operand, registers
        )
        if register_to_update is not None:
            registers[register_to_update] = value_to_update
        if next_pointer is not None:
            pointer = next_pointer
        if next_pointer is None:
            pointer += 2
        if out_value is not None:
            return pointer, instructions, registers, current_out + f"{int(out_value)},"
    return pointer, instructions, registers, current_out


def get_all_out(input_file: str) -> str:
    registers, instructions = read_in_program(input_file)
    pointer = 0
    current_out = ""
    while pointer < len(instructions):
        pointer, instructions, registers, current_out = do_step_until_next_out(
            pointer, instructions, registers, current_out
        )
    return current_out[:-1]


def find_out_for_a(a_start: int, instructions: list[int]) -> str:
    registers = {"A": a_start, "B": 0, "C": 0}
    pointer = 0
    current_out = ""
    while pointer < len(instructions):
        pointer, instructions, registers, current_out = do_step_until_next_out(
            pointer, instructions, registers, current_out
        )
    return current_out[:-1]


def find_exact_copy(input_file: str) -> int:
    _, instructions = read_in_program(input_file)
    pattern_to_match = ",".join(map(str, instructions))
    current_a_options = [0]
    heapq.heapify(current_a_options)
    seen_a = set()
    while current_a_options:
        current_a = heapq.heappop(current_a_options)
        if current_a not in seen_a:
            for i in range(8):
                a_to_check = current_a + i
                if (
                    current_pattern := find_out_for_a(a_to_check, instructions)
                ) in pattern_to_match:
                    heapq.heappush(current_a_options, a_to_check * 8)
                    if len(current_pattern) == len(pattern_to_match):
                        return a_to_check
            seen_a.add(current_a)


if __name__ == "__main__":
    print(get_all_out("day17/day17_final_input.txt"))
    print(find_exact_copy("day17/day17_final_input.txt"))

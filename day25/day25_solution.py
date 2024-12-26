import numpy as np


def read_in_schematics(input_file: str) -> tuple[list, list]:
    with open(input_file) as raw_keys_and_locks:
        keys_and_locks = raw_keys_and_locks.read()
    keys_and_locks = keys_and_locks.split("\n")
    keys = []
    locks = []
    for i in range(0, len(keys_and_locks), 8):
        key_or_lock = []
        for j in range(7):
            key_or_lock.append([*keys_and_locks[i + j]])
        key_or_lock = np.array(key_or_lock)
        key_or_lock_transposed = key_or_lock.T
        key_or_lock_column_heights = tuple(
            np.count_nonzero(column == "#") - 1 for column in key_or_lock_transposed
        )
        if np.count_nonzero(key_or_lock[0] == "#") == 5:
            locks.append(key_or_lock_column_heights)
        else:
            keys.append(key_or_lock_column_heights)
    return keys, locks


def count_fitting_keys(input_file: str) -> int:
    keys, locks = read_in_schematics(input_file)
    total_fits = 0
    for key in keys:
        for lock in locks:
            totals = [key_col + lock_col for (key_col, lock_col) in zip(key, lock)]
            if all(total <= 5 for total in totals):
                total_fits += 1
    return total_fits


if __name__ == "__main__":
    print(count_fitting_keys("day25/day25_final_input.txt"))

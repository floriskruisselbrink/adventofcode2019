def meets_criteria(password: str) -> bool:
    previous = '0'
    has_adjacent = False
    for c in list(password):
        if c < previous:
            return False
        elif c == previous:
            has_adjacent = True
        previous = c

    return has_adjacent


def meets_criteria2(password: str) -> bool:
    previous = '0'
    adjacent_count = 1
    has_two_adjacent = False

    for c in list(password):
        if c < previous:
            return False
        elif c == previous:
            adjacent_count += 1
        else:
            if adjacent_count == 2:
                has_two_adjacent = True
            adjacent_count = 1
        previous = c

    if adjacent_count == 2:
        has_two_adjacent = True

    return has_two_adjacent


def part1():
    found_passwords = 0
    for password in range(153517, 630396):
        if meets_criteria(str(password)):
            found_passwords += 1

    print("Part 1: {}".format(found_passwords))


def part2():
    found_passwords = 0
    for password in range(153517, 630395):
        if meets_criteria2(str(password)):
            found_passwords += 1

    print("Part 2: {}".format(found_passwords))


part1()
part2()

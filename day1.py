from math import floor

from utils import read_input_by_line


def calculate_fuel(mass):
    return floor(mass / 3) - 2


def calculate_fuel2(mass):
    fuel = calculate_fuel(mass)

    fuel_for_fuel = calculate_fuel(fuel)
    while (fuel_for_fuel > 0):
        fuel += fuel_for_fuel
        fuel_for_fuel = calculate_fuel(fuel_for_fuel)

    return fuel


def part1(input_file):
    input = read_input_by_line(input_file)
    total_fuel = 0

    for line in input:
        mass = int(line)
        fuel = calculate_fuel(mass)
        total_fuel += fuel

    print("Part 1 - Total fuel: {}".format(total_fuel))


def part2(input_file):
    input = read_input_by_line(input_file)
    total_fuel = 0

    for line in input:
        mass = int(line)
        fuel = calculate_fuel2(mass)
        total_fuel += fuel

    print("Part 2 - Total fuel: {}".format(total_fuel))


part1('day1.txt')
part2('day1.txt')

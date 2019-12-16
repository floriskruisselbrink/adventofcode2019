from typing import List

from utils import read_line


def chunkstring(string: str, length: int) -> str:
    return (string[0+i:length+i] for i in range(0, len(string), length))


def combine_layers(front: str, back: str) -> str:
    combined = ''
    for i in range(len(front)):
        if front[i] == '2':
            combined += back[i]
        else:
            combined += front[i]
    return combined


def part1():
    image_data = read_line('day8.txt')
    width = 25
    height = 6
    layers = list(chunkstring(image_data, width*height))
    zeroes = [layer.count('0') for layer in layers]

    layer = layers[zeroes.index(min(zeroes))]
    result = layer.count('1') * layer.count('2')
    print(f'Part 1: {result}')


def part2():
    image_data = read_line('day8.txt')
    width = 25
    height = 6
    layers = chunkstring(image_data, width*height)

    result = next(layers)
    for layer in layers:
        result = combine_layers(result, layer)

    result = result.replace('0', ' ')
    result = result.replace('1', '#')

    print('Part2:')
    for row in chunkstring(result, width):
        print(row)


part1()
part2()

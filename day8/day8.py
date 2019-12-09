import os
from typing import List

input_file = os.path.join(os.path.dirname(__file__), 'input.txt')

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
    with open(input_file) as input:
        image_data = input.readline().rstrip()
    width = 25
    height = 6
    layers = list(chunkstring(image_data, width*height))
    zeroes = [layer.count('0') for layer in layers]
    
    layer = layers[zeroes.index(min(zeroes))]
    result = layer.count('1') * layer.count('2')
    print(f'Part 1: {result}')

def part2():
    with open(input_file) as input:
        image_data = input.readline().rstrip()
    width = 25
    height = 6
    layers = list(chunkstring(image_data, width*height))

    result = layers[0]
    for i in range(1, len(layers)):
        result = combine_layers(result, layers[i])
    
    result = result.replace('0', ' ')
    result = result.replace('1', '#')

    print('Part2:')
    for row in chunkstring(result, width):
        print(row)


part1()
part2()
